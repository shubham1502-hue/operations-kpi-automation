import argparse
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_SLA_POLICY = {
    "priority_hours": {
        "Low": 48,
        "Medium": 24,
        "High": 8,
        "Critical": 4,
    },
    "team_priority_hours": {},
}

QUEUE_OWNER_MAPPING = {
    "Support": "Customer Support Lead",
    "Sales Ops": "Revenue Operations Lead",
    "Onboarding": "Customer Onboarding Lead",
    "Shipment": "Fulfillment Operations Lead",
    "Training": "Enablement Lead",
}

UNASSIGNED_OWNER = "Unassigned"


def load_sla_policy(path=None):
    policy = {
        "priority_hours": DEFAULT_SLA_POLICY["priority_hours"].copy(),
        "team_priority_hours": DEFAULT_SLA_POLICY["team_priority_hours"].copy(),
    }
    if not path:
        return policy

    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"SLA policy must be a JSON object: {path}")

    for key in ("priority_hours", "team_priority_hours"):
        if key in raw and not isinstance(raw[key], dict):
            raise ValueError(f"SLA policy field '{key}' must be an object.")

    policy["priority_hours"].update(raw.get("priority_hours", {}))
    policy["team_priority_hours"].update(raw.get("team_priority_hours", {}))
    return policy


def apply_sla_policy(df, policy):
    def target_for_row(row):
        team_rules = policy["team_priority_hours"].get(row["team"], {})
        if row["priority"] in team_rules:
            return team_rules[row["priority"]]
        return policy["priority_hours"].get(row["priority"], row["sla_target_hours"])

    df = df.copy()
    df["sla_target_hours"] = df.apply(target_for_row, axis=1)
    return df


def apply_owner_mapping(df):
    df = df.copy()
    mapped_owners = df["team"].map(QUEUE_OWNER_MAPPING).fillna(UNASSIGNED_OWNER)

    if "owner" in df.columns:
        df["owner"] = df["owner"].fillna("").astype(str).str.strip()
        df["owner"] = np.where(df["owner"] == "", mapped_owners, df["owner"])
    else:
        df["owner"] = mapped_owners

    return df


def rank_queue_breaches(df):
    ticket_volume = df.groupby("team").agg(
        ticket_count=("ticket_id", "size"),
        sampled_months=("month", "nunique"),
    )
    queue_breaches = (
        df.loc[df["breach_hours"] > 0]
        .groupby("team")
        .agg(
            breach_count=("ticket_id", "size"),
            total_breach_hours=("breach_hours", "sum"),
            median_breach_hours=("breach_hours", "median"),
            breach_months=("month", "nunique"),
        )
    )
    ranking = ticket_volume.join(queue_breaches, how="inner").reset_index()
    ranking["breach_rate"] = ranking["breach_count"] / ranking["ticket_count"]
    ranking["share_of_breach_hours"] = (
        ranking["total_breach_hours"] / ranking["total_breach_hours"].sum()
    )
    return ranking.sort_values(
        ["total_breach_hours", "breach_count", "breach_months", "team"],
        ascending=[False, False, False, True],
    ).round({
        "total_breach_hours": 2,
        "median_breach_hours": 2,
        "breach_rate": 4,
        "share_of_breach_hours": 4,
    })


def analyze_ops_data(input_path, output_dir, sla_policy_path=None):

    # -----------------------------
    # Load Data
    # -----------------------------
    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError("Ticket input has no rows.")
    if df["ticket_id"].isna().any() or not df["ticket_id"].is_unique:
        raise ValueError("Use one row per ticket with a populated, unique ticket_id.")

    df = apply_owner_mapping(df)
    df = apply_sla_policy(df, load_sla_policy(sla_policy_path))

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["resolved_at"] = pd.to_datetime(df["resolved_at"])
    if df[["team", "created_at"]].isna().to_numpy().any():
        raise ValueError("Every ticket needs a team and a creation date.")

    hour_columns = ["actual_resolution_hours", "sla_target_hours"]
    hours = df[hour_columns].apply(pd.to_numeric, errors="coerce")
    if not np.isfinite(hours.to_numpy()).all() or hours.lt(0).to_numpy().any():
        raise ValueError("Resolution hours and effective SLA targets must be finite and nonnegative.")
    df[hour_columns] = hours

    # -----------------------------
    # Derived Columns
    # -----------------------------
    df["sla_met"] = np.where(
        df["actual_resolution_hours"] <= df["sla_target_hours"],
        1,
        0
    )

    df["breach_hours"] = np.where(
        df["actual_resolution_hours"] > df["sla_target_hours"],
        df["actual_resolution_hours"] - df["sla_target_hours"],
        0
    )

    df["month"] = df["created_at"].dt.to_period("M").astype(str)

    # -----------------------------
    # 1. KPI SUMMARY
    # -----------------------------
    total_tickets = len(df)
    total_breaches = (df["sla_met"] == 0).sum()
    overall_sla = df["sla_met"].mean()

    monthly_backlog = (
        df.groupby("month")["backlog_flag"]
        .sum()
    )

    avg_monthly_backlog = monthly_backlog.mean()

    kpi_summary = pd.DataFrame({
        "metric": [
            "Overall SLA Compliance %",
            "Total Tickets",
            "Average Monthly Backlog"
        ],
        "value": [
            round(overall_sla, 4),
            total_tickets,
            round(avg_monthly_backlog, 2)
        ]
    })

    # -----------------------------
    # 2. SLA BY TEAM
    # -----------------------------
    sla_by_team = (
        df.groupby(["team", "owner"])
        .agg(
            total_tickets=("ticket_id", "count"),
            sla_met=("sla_met", "sum"),
            avg_resolution_hours=("actual_resolution_hours", "mean"),
            total_breaches=("sla_met", lambda x: (x == 0).sum())
        )
        .reset_index()
    )

    sla_by_team["sla_compliance_rate"] = (
        sla_by_team["sla_met"] / sla_by_team["total_tickets"]
    )

    sla_by_team["avg_resolution_hours"] = (
        sla_by_team["avg_resolution_hours"].round(2)
    )

    sla_by_team["sla_compliance_rate"] = (
        sla_by_team["sla_compliance_rate"].round(4)
    )

    # -----------------------------
    # 3. BACKLOG TREND
    # -----------------------------
    backlog_trend = (
        df.groupby("month")
        .agg(
            total_tickets=("ticket_id", "count"),
            backlog_count=("backlog_flag", "sum")
        )
        .reset_index()
    )

    backlog_trend["backlog_rate"] = (
        backlog_trend["backlog_count"] /
        backlog_trend["total_tickets"]
    ).round(4)

    backlog_by_owner = (
        df.groupby(["owner", "team"])
        .agg(
            total_tickets=("ticket_id", "count"),
            backlog_count=("backlog_flag", "sum")
        )
        .reset_index()
    )

    backlog_by_owner["backlog_rate"] = (
        backlog_by_owner["backlog_count"] /
        backlog_by_owner["total_tickets"]
    ).round(4)

    backlog_by_owner = backlog_by_owner.sort_values(
        "backlog_count",
        ascending=False
    )

    # -----------------------------
    # 4. TOP SLA BREACHES
    # -----------------------------
    top_sla_breaches = (
        df[df["breach_hours"] > 0]
        .sort_values("breach_hours", ascending=False)
        .head(10)
        [
            [
                "ticket_id",
                "team",
                "owner",
                "priority",
                "actual_resolution_hours",
                "sla_target_hours",
                "breach_hours"
            ]
        ]
    )

    queue_breaches = rank_queue_breaches(df)
    top_queue = queue_breaches.iloc[0] if not queue_breaches.empty else None

    latest_backlog = backlog_trend.iloc[-1]["backlog_count"] if not backlog_trend.empty else 0
    first_backlog = backlog_trend.iloc[0]["backlog_count"] if not backlog_trend.empty else 0
    backlog_delta = latest_backlog - first_backlog
    top_breach = top_sla_breaches.iloc[0] if not top_sla_breaches.empty else None

    # -----------------------------
    # Export
    # -----------------------------
    os.makedirs(output_dir, exist_ok=True)

    kpi_summary.to_csv(f"{output_dir}/kpi_summary.csv", index=False, lineterminator="\n")
    sla_by_team.to_csv(f"{output_dir}/sla_by_team.csv", index=False, lineterminator="\n")
    backlog_trend.to_csv(f"{output_dir}/backlog_trend.csv", index=False, lineterminator="\n")
    backlog_by_owner_path = f"{output_dir}/backlog_by_owner.csv"
    backlog_by_owner.to_csv(backlog_by_owner_path, index=False, lineterminator="\n")
    top_sla_breaches.to_csv(f"{output_dir}/top_sla_breaches.csv", index=False, lineterminator="\n")
    queue_breaches.to_csv(f"{output_dir}/sla_breach_drivers.csv", index=False, lineterminator="\n")
    write_executive_summary(
        output_path=f"{output_dir}/executive_summary.md",
        total_tickets=total_tickets,
        total_breaches=total_breaches,
        overall_sla=overall_sla,
        avg_monthly_backlog=avg_monthly_backlog,
        backlog_delta=backlog_delta,
        top_queue=top_queue,
        top_breach=top_breach,
    )

    if not os.path.isfile(backlog_by_owner_path):
        raise RuntimeError(f"Expected backlog by owner output at {backlog_by_owner_path}")

    # -----------------------------
    # Sanity Print
    # -----------------------------
    print("-- Analysis Summary --------------------------")
    print(f"Total Tickets       : {total_tickets:,}")
    print(f"Total Breaches      : {total_breaches:,}")
    print(f"Overall Compliance  : {round(overall_sla*100,2)}%")
    print(f"Avg Monthly Backlog : {round(avg_monthly_backlog,2)}")
    largest_breach_hours = top_breach["breach_hours"] if top_breach is not None else 0
    print(f"Top Breach (hrs)    : {largest_breach_hours:.2f}")


def write_executive_summary(
    output_path,
    total_tickets,
    total_breaches,
    overall_sla,
    avg_monthly_backlog,
    backlog_delta,
    top_queue,
    top_breach,
):
    backlog_direction = "increased" if backlog_delta > 0 else "decreased" if backlog_delta < 0 else "stayed flat"

    if top_queue is not None:
        queue_summary = (
            f"{top_queue['team']} contributed {top_queue['total_breach_hours']:,.2f} over-target "
            f"hours ({top_queue['share_of_breach_hours']:.1%} of the sample total). "
            f"It had {top_queue['breach_count']:,} breaches across {top_queue['ticket_count']:,} tickets "
            f"({top_queue['breach_rate']:.2%}), with breaches in {top_queue['breach_months']} of "
            f"{top_queue['sampled_months']} ticket-creation months. "
            f"The median breached ticket ran {top_queue['median_breach_hours']:.2f} hours over target."
        )
        recommended_action = (
            f"Start with the {top_queue['team']} queue. Use the team scorecard to identify the owner, "
            "then compare SLA misses by priority and period. Review ticket histories, workload, and "
            "staffing to test possible routing, capacity, or escalation causes."
        )
    else:
        queue_summary = "No SLA breaches were found in the current dataset."
        recommended_action = "Keep the current SLA review cadence and track backlog-flagged tickets."

    individual_summary = "Every ticket met its SLA target."
    if top_breach is not None:
        individual_summary = (
            f"Ticket {top_breach['ticket_id']} in {top_breach['team']} ran "
            f"{top_breach['breach_hours']:.2f} hours over its {top_breach['priority']} priority target."
        )

    lines = [
        "# Operations KPI Executive Summary",
        "",
        "## KPI snapshot",
        "",
        f"- Total tickets analyzed: {total_tickets:,}",
        f"- SLA compliance: {overall_sla:.2%}",
        f"- Total SLA breaches: {total_breaches:,}",
        f"- An average of {round(avg_monthly_backlog, 2):,} backlog-flagged tickets per month",
        "",
        "## Backlog trend",
        "",
        f"The count of backlog-flagged tickets {backlog_direction} by {abs(int(backlog_delta)):,} "
        "from the first to the latest ticket-creation month in the sample.",
        "",
        "## Queue SLA breach burden",
        "",
        queue_summary,
        "",
        "## Largest individual SLA breach",
        "",
        individual_summary,
        "",
        "## Recommended action",
        "",
        recommended_action,
        "",
    ]

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    if not os.path.isfile(output_path):
        raise RuntimeError(f"Expected executive summary at {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze operations KPI data.")
    parser.add_argument("--input", default="data/ops_tickets.csv", help="Ticket CSV path.")
    parser.add_argument("--out", default="data", help="Output directory.")
    parser.add_argument("--sla-policy", help="Optional JSON file with SLA thresholds.")
    args = parser.parse_args()

    analyze_ops_data(
        input_path=args.input,
        output_dir=args.out,
        sla_policy_path=args.sla_policy,
    )
