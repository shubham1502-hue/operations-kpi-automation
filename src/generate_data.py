import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_ops_tickets(n=80000, out_dir="data", seed=42):

    np.random.seed(seed)
    random.seed(seed)

    teams = ["Support", "Sales Ops", "Onboarding", "Shipment", "Training"]
    regions = ["India", "EMEA", "APAC", "Americas"]
    priorities = ["Low", "Medium", "High", "Critical"]

    # Realistic SLA targets
    sla_targets = {
        "Low": 48,
        "Medium": 24,
        "High": 8,
        "Critical": 4
    }

    # Realistic breach probabilities
    breach_probability = {
        "Low": 0.05,
        "Medium": 0.10,
        "High": 0.18,
        "Critical": 0.25
    }

    start = datetime(2025, 1, 1)

    rows = []

    for i in range(n):

        created = start + timedelta(minutes=random.randint(0, 60*24*300))

        priority = random.choices(
            priorities,
            weights=[45, 35, 15, 5]
        )[0]

        team = random.choice(teams)
        region = random.choice(regions)

        sla_target = sla_targets[priority]

        # Decide if ticket breaches
        breached = random.random() < breach_probability[priority]

        if not breached:
            # Resolved within SLA window
            actual_hours = np.random.uniform(
                0.5 * sla_target,
                0.95 * sla_target
            )
        else:
            # Slight breach, not catastrophic
            actual_hours = np.random.uniform(
                1.05 * sla_target,
                1.5 * sla_target
            )

        resolved = created + timedelta(hours=float(actual_hours))

        backlog_flag = 1 if random.random() < 0.15 else 0

        rows.append({
            "ticket_id": f"T{i+1:06d}",
            "created_at": created.strftime("%Y-%m-%d %H:%M:%S"),
            "resolved_at": resolved.strftime("%Y-%m-%d %H:%M:%S"),
            "team": team,
            "region": region,
            "priority": priority,
            "sla_target_hours": sla_target,
            "actual_resolution_hours": round(actual_hours, 2),
            "backlog_flag": backlog_flag
        })

    df = pd.DataFrame(rows)

    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "ops_tickets.csv")

    df.to_csv(output_path, index=False)

    # Print sanity stats
    breach_rate = (
        (df["actual_resolution_hours"] > df["sla_target_hours"]).mean()
    )

    print(f"Saved: {output_path}  ({len(df):,} rows)")
    print("── Summary ──────────────────────────────")
    print(f"  SLA breach rate : {round(breach_rate*100,2)}%")
    print(f"  SLA compliance  : {round((1-breach_rate)*100,2)}%")
    print(f"  Backlog flagged : {df['backlog_flag'].sum():,}")

if __name__ == "__main__":
    generate_ops_tickets(
        n=80000,
        out_dir="/Users/vegitto/Desktop/projects/operations-kpi-automation/data"
    )