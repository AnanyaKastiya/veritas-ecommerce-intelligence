# Veritas E-Commerce Intelligence

The Veritas E-Commerce Intelligence engine was developed for the Accenture
Innovation Challenge as an autonomous e-commerce KPI diagnosis, root-cause
machine learning attribution, and prescriptive decisioning platform. It
transforms reactive dashboards into an autonomous decision cockpit by
decomposing metric drops into Volume, Mix, and Friction drivers,
cross-examining telemetry via an AI Tribunal, and generating closed-loop
prescriptive playbooks.

A production build is deployed and accessible at the
[live demo application](https://veritas-ceg2.onrender.com). For a full
description of the platform and architecture, visit the
[project repository](https://github.com/AnanyaKastiya/veritas-ecommerce-intelligence).
Submit bug reports and feature suggestions, or track changes in the
[issue queue](https://github.com/AnanyaKastiya/veritas-ecommerce-intelligence/issues).


## Table of contents

- Requirements
- Recommended modules
- Installation
- Configuration
- Troubleshooting
- FAQ
- Maintainers


## Requirements

This platform requires the following dependencies:

- [Python 3.10](https://www.python.org/downloads/) or higher
- [Pandas](https://pandas.pydata.org/) (version 2.0.0 or higher)
- [NumPy](https://numpy.org/) (version 1.24.0 or higher)
- Modern web browser with ECMAScript 6 support (Chrome, Edge, Firefox, Safari)


## Recommended modules

- [Google GenAI SDK](https://pypi.org/project/google-genai/): When enabled with
    a valid API key, provides advanced natural language Q&A and narrative
    persona synthesis.
- [Tailwind CSS CDN](https://tailwindcss.com/): Included out-of-the-box for
    responsive dark-mode rendering.


## Installation

The quickest way to explore the platform is to visit the
[live demo application](https://veritas-ceg2.onrender.com).

To run the application locally:

1. Clone this repository locally:
    ```bash
    git clone https://github.com/AnanyaKastiya/veritas-ecommerce-intelligence.git
    cd veritas-ecommerce-intelligence
    ```
1. Ensure Python 3.10+ is installed and accessible in your PATH.
1. Launch the platform server using the Windows batch launcher:
    ```cmd
    run_app.bat
    ```
1. Alternatively, launch the backend server directly via Python:
    ```bash
    python backend/server.py
    ```
1. Open your web browser and navigate to `http://localhost:8000/`.


## Configuration

1. Choose your analytical role in the top header:
    - **👔 Business Manager**: Executive summaries, P&L financial margin drag,
        and one-click action approvals.
    - **📊 Data Analyst**: Deep statistical audits, exact z-scores, Shapley
        variance shares, and end-to-end SQL DAG lineage.
1. Ingest reference or custom datasets:
    - The platform automatically initializes with 100,000+ orders from the
        reference Olist Brazilian E-Commerce dataset.
    - To ingest custom data, click `+ Upload Data (Single / Multi-File)`.
    - Select single or multiple CSV tables (`orders.csv`, `order_items.csv`,
        `products.csv`). The canonical semantic layer automatically detects
        keys and joins relational tables in memory.
1. Navigate across the 7 cockpit sections using the top navigation bar:
    - Section 1: Overview & KPI Health Monitoring
    - Section 2: KPI Explorer (What, Where, When, Who Slicers)
    - Section 3: Root-Cause Driver Analysis & The AI Courtroom (Tribunal)
    - Section 4: Evidence & Lineage Panel (Freshness Matrix & SQL DAG)
    - Section 5: Action Center & Closed-Loop Realization Tracker
    - Section 6: Ask the Engine (Natural Language Business Q&A)
    - Section 7: Feedback Loop & Continuous Calibration
1. Test competition challenge scenarios using the scenario buttons:
    - **🎯 Scenario 1: Multi-Factor KPI Attribution**: Decomposes an -8.4%
        weekly revenue decline into Volume (51%), Mix (24%), and Payment (15%).
    - **⚠️ Scenario 2: Contradictory Telemetry & Active Abstention**:
        Demonstrates active abstention when telemetry is stale or contradictory
        (41% confidence) with human-in-the-loop diagnostic polling.
    - **🚀 Scenario 3: Sparse History & New Product Launch**: Interactive
        observation window sandbox illustrating early ramp (< 7 days) false
        alarm suppression and Category Peer Cohort Proxy Benchmarks.


## Troubleshooting

If you encounter issues during installation or runtime, check the following:

- **Server fails to bind to port 8000**:
    Verify that no other application is using port 8000, or modify the port
    parameter in `backend/server.py`.
- **Uploaded CSV fails to map**:
    Ensure the CSV file contains a numeric value column (e.g. `price`, `gmv`,
    `sales`, `revenue`, `amount`) and is comma, semicolon, or tab-delimited.
- **Console encoding warnings on Windows**:
    Ensure your terminal supports UTF-8 encoding by executing `chcp 65001`
    prior to launching the server.


## FAQ

**Q: Does Veritas use LLMs to calculate revenue drop percentages or Shapley
values?**

**A:** No. Under the strict quantitative architecture, all arithmetic,
percentages, and statistical z-scores are computed deterministically via
Python algorithms. LLMs are strictly confined to natural language synthesis and
intent classification.

**Q: Can I upload multiple relational CSV files at the same time?**

**A:** Yes. The universal ingestion modal supports selecting multiple CSV files
simultaneously (`orders.csv`, `order_items.csv`, `products.csv`). The canonical
semantic layer automatically joins them on common entity keys (`order_id`,
`product_id`).

**Q: How do I switch between the Business Manager and Data Analyst views?**

**A:** Click the `👔 Manager` or `📊 Analyst` buttons in the top-right header
bar. The entire interface updates immediately with role-tailored narratives,
appropriate data granularity, and RBAC security masking.

**Q: What methodology powers the AI Courtroom?**

**A:** The Tribunal cross-examines evidence across three distinct agents: the
Internal Operational Detective (customer reviews and logistics logs), Market &
Context Spy (promotional campaigns and competitor elasticity), and Data
Integrity Sentry (schema and database replica validation), establishing a 94%
calibrated burden of proof.


## Maintainers

- Ananya Kastiya - [AnanyaKastiya](https://github.com/AnanyaKastiya)
- Osheen Dongre - [Osheen145](https://github.com/Osheen145)
