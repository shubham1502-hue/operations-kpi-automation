# Operations KPI Automation - SLA & Backlog Analytics

## Overview
This project simulates an operations ticketing system (80,000 tickets) and builds an end-to-end analytics pipeline to evaluate SLA compliance and backlog performance.

The pipeline:
1. Generates realistic ticket-level operational data
2. Computes SLA compliance at ticket level
3. Aggregates team-level and monthly KPIs
4. Exports analysis-ready datasets for BI visualization (Tableau)

## Key Metrics
- Overall SLA Compliance: 90.4%
- Total Tickets: 80,000
- Average Monthly Backlog: 1,213

## Technical Approach
- SLA compliance calculated at ticket level to avoid aggregation distortion
- Weighted compliance aggregation at team level
- Controlled breach probability simulation for realistic modeling
- Clean separation between data engineering and BI layer

## Project Structure
- `src/generate_data.py` – Simulates ticket data
- `src/analysis.py` – Computes KPIs and exports summary tables
- `data/` – Generated datasets
- `dashboard/` – Tableau dashboard screenshot

## Business Insight
Shipment team shows marginally lower SLA compliance relative to organizational average, indicating potential process inefficiencies requiring operational deep dive.

## Tools Used
- Python (pandas, numpy)
- Tableau Public
- GitHub for version control