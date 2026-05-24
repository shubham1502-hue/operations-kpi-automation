# Operations KPI Command Center

Operations KPI workflow for SLA compliance, backlog risk, breach drivers, and team-level execution visibility.

<!-- FOUNDER_OS_STANDARD_README -->

## Portfolio role

This is a supporting operations KPI automation repo. It is useful for showing SLA policy logic, backlog visibility, breach driver analysis, and founder-ready weekly ops summaries. It supports the portfolio as an operations analytics proof point, not as a flagship Founder OS module.

## The founder problem

Ops-heavy startups can have ticket data but still miss the operating picture: where SLAs are slipping, which teams are overloaded, and what needs intervention before customers feel the problem.

## What this repo does

- generates sample operations ticket data
- analyzes SLA and backlog metrics
- exports KPI summary files
- creates dashboard-ready artifacts

## What a founder gets in 10 minutes

- KPI summary CSV
- executive summary Markdown
- SLA by team output
- top breach drivers
- backlog trend data
- backlog by owner output
- dashboard preview

## Before and after

Before:

- ticket exports with no owner
- manual SLA reporting
- backlog surprises
- unclear breach drivers

After:

- repeatable ops review
- team-level SLA view with owners
- breach driver list
- dashboard-ready outputs

## Who this is for

- operations leads
- early-stage founders
- Founder's Office teams
- BizOps operators
- service delivery teams

## Quick start

- Run `python3 -m pip install -r requirements.txt`.
- Run `python3 src/generate_data.py`.
- Run `python3 src/analysis.py`.
- Optionally run `python3 src/analysis.py --sla-policy config/sla_policy.json`.
- Open `data/kpi_summary.csv` first.

## How to fork and use this for your company

1. Click Fork.
2. Rename the repo if needed.
3. Replace `data/ops_tickets.csv` with your ticket export.
4. Update SLA thresholds in `config/sla_policy.json` and team mappings in `src/analysis.py`.
5. Run the analysis before the weekly operations review.
6. Move outputs into Google Sheets, Notion, Airtable, Linear, Asana, ClickUp, or your BI tool.

### Non-technical path

- Replace one CSV: `data/ops_tickets.csv`.
- Edit one threshold section in `src/analysis.py` if needed.
- Run two commands.
- Read one output first: `data/kpi_summary.csv`.

## Input format

- ticket ID
- team
- owner
- status
- created date
- resolved date
- SLA target
- priority
- breach reason
- optional JSON SLA policy config

The default sample data and examples are synthetic, anonymized, or template-only unless the repo explicitly documents a public source. Keep private customer, prospect, employee, investor, borrower, merchant, payment, or company data out of public forks.

## Output files

- `data/kpi_summary.csv`: top-line ops KPIs
- `data/executive_summary.md`: founder-ready weekly operations summary
- `data/sla_by_team.csv`: team SLA performance
- `data/top_sla_breaches.csv`: breach drivers
- `data/backlog_trend.csv`: backlog trend
- `data/backlog_by_owner.csv`: backlog accountability by queue owner
- `dashboard/SLA_Backlog_Dashboard.png`: dashboard preview

## Owner mapping

`src/analysis.py` maps each queue in the `team` column to an accountable owner. If your input CSV already includes an `owner` column, the script keeps that value and only fills blanks from the mapping.

| Team | Default owner |
| --- | --- |
| Support | Customer Support Lead |
| Sales Ops | Revenue Operations Lead |
| Onboarding | Customer Onboarding Lead |
| Shipment | Fulfillment Operations Lead |
| Training | Enablement Lead |

Sample owner-aware outputs:

| Output | Owner field |
| --- | --- |
| `data/sla_by_team.csv` | `owner` next to each team scorecard row |
| `data/top_sla_breaches.csv` | `owner` next to each breach driver |
| `data/backlog_by_owner.csv` | `owner`, `team`, `backlog_count`, and `backlog_rate` |

## Example founder workflow

- Monday: refresh ticket export.
- Tuesday: run KPI analysis.
- Wednesday: review breach drivers.
- Thursday: assign operational fixes.
- Friday: update weekly operating review with decisions.

## Customization guide

Customize these before using the repo for a real company:

- SLA thresholds
- team names
- breach categories
- priority rules
- dashboard columns

## Where this fits in the Founder OS

This is the operations execution layer. Pair it with `founder-weekly-operating-review-agent` for weekly cadence and `revops-infrastructure-playbook` for handoff and reporting design.

## Why this matters

This is not a screenshot dashboard. It is a repeatable operations review workflow for deciding where to intervene.

## Roadmap

- Google Sheets export
- Slack SLA alerts
- Linear and Asana sync
- Streamlit dashboard
- weekly review integration

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) if present. Practical improvements are welcome when they make the workflow easier to fork, run, or adapt.

## License

MIT License. See [LICENSE](LICENSE).

## Built by

Built by Shubham Singh, a founder-facing operator focused on RevOps, GTM systems, startup metrics, AI workflows, and operating systems for early-stage teams.

## Use this in your company

Fork it, replace the sample inputs with your company context, and run the workflow. Start with the main output listed in the Quick Start section. Keep private data out of public forks.

## If you are a Founder's Office candidate

Use this repo to understand how a founder-facing operator turns messy inputs into decisions, cadence, and execution artifacts. Fork it, adapt it to a real company example, and write a short case note explaining what changed.

---

## Detailed implementation notes

The founder-facing guide above is the fastest path. The original repo-specific notes are preserved below for deeper implementation context.

A founder/operator command center for service delivery health, SLA compliance, backlog risk, breach drivers, and team-level execution visibility.

Early-stage teams lose control of service delivery when SLA breaches, backlog growth, ownership gaps, and execution bottlenecks are scattered across tickets, sheets, and manual reports. This repo turns ticket lifecycle data into a repeatable operations review system that helps founders, ops leads, service delivery teams, and Founder's Office operators see where execution is breaking down and where to intervene first.

## Problem

Ops-heavy startups often have the raw data but not the operating cadence:

- SLA breaches are discovered after escalations.
- Backlog growth is reviewed manually instead of monitored weekly.
- Team-level ownership gaps are hidden inside ticket exports.
- Leaders debate symptoms without a clean view of breach drivers.
- Dashboard work depends on ad hoc data pulls instead of a reusable pipeline.

This project shows how to convert ticket operations data into leadership-ready KPIs, scorecards, and Tableau-ready exports.

## What This Repo Includes

- `src/generate_data.py`: generates a synthetic 80,000-row operations ticket dataset.
- `src/analysis.py`: computes SLA compliance, backlog trends, owner mappings, team scorecards, and top breach records.
- `data/ops_tickets.csv`: sample ticket lifecycle dataset.
- `data/kpi_summary.csv`: summary KPI output.
- `data/executive_summary.md`: founder-ready Markdown summary output.
- `data/sla_by_team.csv`: team-level SLA scorecard output.
- `data/backlog_trend.csv`: monthly backlog trend output.
- `data/backlog_by_owner.csv`: backlog accountability output by owner and team.
- `data/top_sla_breaches.csv`: ticket-level breach driver output.
- `dashboard/SLA_Backlog_Dashboard.png`: dashboard preview image.
- `requirements.txt`: Python package requirements.
- `LICENSE`: MIT license for reuse.

The CSV files are tracked as sample portfolio outputs. If you regenerate them, review the diff before committing refreshed outputs.

## System Workflow

1. Generate or replace ticket lifecycle data.
2. Calculate SLA status and breach hours.
3. Summarize operational health into KPI, backlog, and team-level outputs.
4. Review breach drivers by team, priority, and resolution time.
5. Load the exports into Tableau or another BI layer for weekly ops review.
6. Use the scorecards to decide where founders or ops leads should intervene.

## KPI Logic

The repo models a service delivery workflow with ticket-level SLA targets:

```text
Ticket Created -> Ticket Resolved -> SLA Met / SLA Breached -> Backlog Flag -> Team Scorecard
```

Core logic:

- SLA met = actual resolution hours <= SLA target hours.
- Breach hours = actual resolution hours - SLA target hours when resolution exceeds target.
- Overall SLA compliance = tickets meeting SLA / total tickets.
- Average monthly backlog = average monthly count of backlog-flagged tickets.
- Team scorecard = ticket volume, SLA-met count, average resolution hours, total breaches, owner, and SLA compliance rate by team.
- Owner backlog = backlog-flagged tickets grouped by owner and team.
- Top breach drivers = highest breach-hour tickets with team, owner, priority, actual resolution hours, and SLA target.

Current sample outputs show:

- 80,000 tickets analyzed.
- 90.4% SLA compliance.
- 1,213 average monthly backlog.
- Teams monitored: Onboarding, Sales Ops, Shipment, Support, and Training.

## Example Operator Use Cases

- Founder weekly ops review: identify which team or workflow is creating the most service delivery risk.
- Support operations: monitor SLA compliance and backlog pressure before customer escalations compound.
- Service delivery leadership: compare team-level execution health across queues.
- Founder's Office operating cadence: turn raw ticket exports into a weekly intervention list.
- Board or investor prep: summarize operational discipline with concrete SLA and backlog metrics.
- Tableau reporting: refresh BI-ready CSV outputs for a simple SLA/backlog dashboard.

## Use This In Your Company

1. Replace the sample ticket data with a Zendesk, Intercom, HubSpot, Jira, Linear, Freshdesk, or spreadsheet export.
2. Map your ticket fields to the current schema: team, region, priority, SLA target, resolution hours, and backlog flag.
3. Update `QUEUE_OWNER_MAPPING` in `src/analysis.py` so each queue has an accountable owner.
4. Tune SLA thresholds so they match your customer promise and internal service levels.
5. Run the analysis before your weekly operations review.
6. Review the team scorecard, owner backlog, and top breach list with named owners.
7. Assign interventions for the highest-risk queue or breach driver.
8. Refresh the dashboard only after the CSV outputs are validated.

## Minimum Edits Before First Use

| Edit | Where | Why |
| --- | --- | --- |
| Replace ticket data | `data/ops_tickets.csv` or `src/generate_data.py` | Use your real ticket lifecycle, queue, team, priority, and resolution fields. |
| Map lifecycle fields | `src/analysis.py` | Align KPI logic with your ticketing system's column names and workflow. |
| Map queue owners | `QUEUE_OWNER_MAPPING` in `src/analysis.py` | Assign one accountable owner to every team or queue. |
| Tune SLA thresholds | `config/sla_policy.json` | Match what your company considers low, medium, high, and critical service commitments. |
| Update backlog definition | `src/analysis.py` | Backlog should reflect your real operating risk, not just a sample flag. |
| Refresh BI outputs | `data/*.csv` | Keep Tableau or other reporting layers aligned with the latest analysis. |
| Update dashboard view | `dashboard/SLA_Backlog_Dashboard.png` or your BI tool | Reflect your real teams, queues, and review cadence. |

## How To Run / Use

Install dependencies:

```bash
pip install -r requirements.txt
```

Run from the repo root:

```bash
python3 src/generate_data.py
python3 src/analysis.py
```

The scripts write CSV outputs into `data/`. Because this repo includes sample CSV outputs for portfolio review, running the scripts may modify tracked files. Commit refreshed CSVs only when you intentionally want to update the sample dataset and dashboard inputs.

## SLA Policy Config

Defaults still work without a policy file. To tune SLA promises without editing code, copy `config/sla_policy.json`, adjust the thresholds, and run:

```bash
python3 src/analysis.py --sla-policy config/sla_policy.json
```

Supported sections:

- `priority_hours`: default SLA target hours by priority.
- `team_priority_hours`: optional team-specific overrides by priority.

Team-specific overrides win over the default priority threshold. If a priority is not listed, the script keeps the CSV's existing `sla_target_hours` value.

## Outputs

- `data/kpi_summary.csv`: overall SLA compliance, total tickets, and average monthly backlog.
- `data/executive_summary.md`: weekly Markdown summary with SLA compliance, backlog trend, top breach driver, and recommended action.
- `data/sla_by_team.csv`: team-level ticket count, SLA-met count, average resolution hours, breaches, and compliance rate.
- `data/backlog_trend.csv`: monthly ticket volume, backlog count, and backlog rate.
- `data/backlog_by_owner.csv`: backlog count and backlog rate by owner and team.
- `data/top_sla_breaches.csv`: top ticket-level SLA breaches by breach hours.
- `dashboard/SLA_Backlog_Dashboard.png`: static dashboard preview for the SLA/backlog reporting layer.

## Folder Structure

```text
.
|-- dashboard/
|  `-- SLA_Backlog_Dashboard.png
|-- data/
|  |-- backlog_by_owner.csv
|  |-- backlog_trend.csv
|  |-- executive_summary.md
|  |-- kpi_summary.csv
|  |-- ops_tickets.csv
|  |-- sla_by_team.csv
|  `-- top_sla_breaches.csv
|-- src/
|  |-- analysis.py
|  `-- generate_data.py
|-- .gitignore
|-- LICENSE
|-- README.md
`-- requirements.txt
```

## Customization Guide

- For support teams: map ticket source, customer tier, escalation reason, and first response time.
- For onboarding teams: replace ticket priority with onboarding phase, customer segment, or launch risk.
- For fulfillment or shipment ops: map SLA targets to delivery promise, dispatch delay, or exception handling time.
- For sales ops: track lead routing, quote turnaround, contract ops tasks, and queue aging.
- For Founder's Office cadence: add owner, intervention, due date, and next review status to the scorecard.

Keep the operating loop simple: measure SLA health, find backlog risk, isolate breach drivers, assign owners, and review progress weekly.

## Portfolio Note

This repo is part of a Founder's Office / startup operator portfolio focused on practical operating systems for early-stage companies. It demonstrates how an operator can move from messy service delivery data to KPI visibility, execution scorecards, and founder-level intervention areas.
