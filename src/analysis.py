import pandas as pd
import numpy as np
import os


def analyze_ops_data(input_path, output_dir):

    # -----------------------------
    # Load Data
    # -----------------------------
    df = pd.read_csv(input_path)

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["resolved_at"] = pd.to_datetime(df["resolved_at"])

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
        df.groupby("team")
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
                "priority",
                "actual_resolution_hours",
                "sla_target_hours",
                "breach_hours"
            ]
        ]
    )

    # -----------------------------
    # Export
    # -----------------------------
    os.makedirs(output_dir, exist_ok=True)

    kpi_summary.to_csv(f"{output_dir}/kpi_summary.csv", index=False)
    sla_by_team.to_csv(f"{output_dir}/sla_by_team.csv", index=False)
    backlog_trend.to_csv(f"{output_dir}/backlog_trend.csv", index=False)
    top_sla_breaches.to_csv(f"{output_dir}/top_sla_breaches.csv", index=False)

    # -----------------------------
    # Sanity Print
    # -----------------------------
    print("── Analysis Summary ──────────────────────────")
    print(f"Total Tickets       : {total_tickets:,}")
    print(f"Total Breaches      : {total_breaches:,}")
    print(f"Overall Compliance  : {round(overall_sla*100,2)}%")
    print(f"Avg Monthly Backlog : {round(avg_monthly_backlog,2)}")
    print(f"Top Breach (hrs)    : {round(top_sla_breaches['breach_hours'].max(),2)}")


if __name__ == "__main__":

    analyze_ops_data(
        input_path="/Users/vegitto/Desktop/projects/operations-kpi-automation/data/ops_tickets.csv",
        output_dir="/Users/vegitto/Desktop/projects/operations-kpi-automation/data"
    )