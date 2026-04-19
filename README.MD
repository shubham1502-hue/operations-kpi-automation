# Operations KPI Automation — SLA & Backlog Analytics

**End-to-end operational analytics pipeline** tracking 80,000 ticket 
lifecycles across 5 teams. Monitors SLA compliance, identifies breach 
drivers, and surfaces backlog trends for operational decision-making.

Built to simulate the kind of self-serve reporting infrastructure that 
ops and support teams rely on to manage performance without depending 
on ad hoc data pulls.

---

## Key Results

| Metric | Value |
|---|---|
| Tickets Analyzed | 80,000 |
| SLA Compliance Rate | 90.4% |
| Average Backlog | 1,213 tickets |
| Teams Monitored | Onboarding, Sales Ops, Shipment, Support, Training |

---

## What It Does

- **SLA breach detection** — flags tickets exceeding thresholds by team and priority
- **Backlog trend monitoring** — moving average + monthly volume to isolate demand spikes
- **Team-level compliance scoring** — ranked view to identify lowest-performing queues
- **Breach root cause view** — individual ticket drill-down with breach hours by department

---

## Dashboard Preview

![SLA & Backlog Dashboard](dashboard/SLA_Backlog_Dashboard.png)

🔗 **[Open Live Tableau Dashboard](https://public.tableau.com/views/SLABacklog/Dashboard1)**

---

## Tech Stack

`Python` · `Pandas` · `Tableau Public` · `Git`

**Pipeline:**
1. Synthetic data generation with weighted SLA distribution
2. KPI computation and breach modeling
3. Automated export of BI-ready datasets
4. Tableau dashboard visualization

---

## How to Run

```bash
python src/generate_data.py
python src/analysis.py
```

---

## Strategic Context

Simulates real-world operational reporting workflows used in 
large-scale e-commerce and ops-heavy startups where support team 
SLA visibility drives staffing, escalation, and process decisions.

---

*Part of a portfolio targeting analyst roles at Series A+ startups.*  
*[← Back to Profile](https://github.com/shubham1502-hue)*
