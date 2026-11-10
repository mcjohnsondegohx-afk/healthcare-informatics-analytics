# Healthcare Access & Scheduling Analytics

A reproducible demonstration project for **health informatics, healthcare data analytics, and hospital operations**.

**Important: This is a portfolio demonstration using 1,200 fully synthetic appointment records. No real patient information or protected health information (PHI) is included.** Findings are not claims about an actual hospital.

## The business question
How might hospital operations teams use scheduling and check-in data to identify missed-appointment patterns and potential areas for workflow improvement?

## Contents
* `synthetic_appointments.csv`: 1,200 simulated appointments across 3 fictional facilities and 4 specialties, Jan–June 2026.
* `hospital_access_demo.db`: ready-to-query SQLite database.
* `analytics_queries.sql`: SQL for KPIs, facility variation, specialty variation, and scheduling lead times.
* `dashboard_preview.png`: redesigned portfolio-ready executive dashboard with 4 KPIs, monthly trends, facility comparison, specialty rates, lead-time analysis and decision-oriented insights.
* `interactive_dashboard.html`: fully interactive offline dashboard. Open directly in your browser to filter by facility, specialty, or month. No installation or server required.
* `build_dashboard.py`: regenerates the advanced dashboard preview and offline HTML from the CSV.
* `run_analysis.py`: regenerates a basic text analysis and the original two-chart analysis view (named `basic_analysis.png`).

## Sample results from the synthetic data
* **1,200 appointments**
* **249 no-shows**, **20.8%** simulated no-show rate
* **14.3 minutes** mean check-in wait among completed appointments

These patterns are intentionally simulated. They suggest hypotheses to investigate, not causal findings.

## Reproduce locally
1. Open `interactive_dashboard.html` in a browser and use the facility, specialty, and month filters. It is self contained and works offline.
2. To regenerate the executive dashboard, install Python 3 and dependencies: `python3 -m pip install pandas matplotlib plotly`.
3. Run `python3 build_dashboard.py` from this project directory.
4. Open `analytics_queries.sql` and execute it against `hospital_access_demo.db` using SQLite or a compatible SQL client.
5. To create a Power BI version, import `synthetic_appointments.csv`, create a No-show Rate measure, and compare rates by facility, specialty, and lead-time band.

## Suggested Power BI measures
```dax
Appointments = COUNTROWS(Appointments)
No Shows = CALCULATE(COUNTROWS(Appointments), Appointments[status] = "No Show")
No Show Rate = DIVIDE([No Shows], [Appointments], 0)
Average Check-in Wait = AVERAGE(Appointments[checkin_wait_minutes])
```

## Questions to ask before acting on real data
Are definitions of no-shows consistent across sites? Are appointment cancellations excluded? Are patient access constraints, scheduling policies, and appointment mix confounders? Are small subgroups sufficiently large for reliable comparisons? Can analysts report aggregates while protecting patient privacy?

## Candidate process improvements to evaluate
Test reminder timing, review appointment lead times, compare scheduling workflows, and validate potential differences with actual data and clinical operations staff. Do not conclude that lead time *causes* missed appointments from this simulation.

## Resume / LinkedIn Transperency
This project was developed as a personal portfolio initiative to explore the application of data analytics and information technology within healthcare operations. It uses entirely synthetic patient scheduling data to demonstrate SQL querying, Python analysis, interactive dashboards, and healthcare performance reporting.

The project serves as a foundation for continued hands-on learning in health informatics, with a focus on data accuracy, operational efficiency, and evidence-based decision-making.

All findings are based on simulated data and do not represent actual healthcare facilities or patient outcomes.

## Live dashboard
This repository includes `index.html` for GitHub Pages. Enable **Settings > Pages > Deploy from a branch > main > /(root)**, then use the public Pages URL. The dashboard visualizes synthetic data only.
