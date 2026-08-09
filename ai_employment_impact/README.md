# AI Impact on Employment

## Dataset

`ai_job_impact.csv` - 2000 employees, 17 columns. Salary, job status and
satisfaction recorded around the adoption of AI in each employee's industry.

## Variable types

**Quantitative:** Age, Years_Experience, Salary_Before_AI, Salary_After_AI,
Work_Hours_Per_Week, Job_Satisfaction (1-10 scale), Productivity_Change_%

**Qualitative:** Employee_ID (identifier), Gender, Education_Level, Industry, Job_Role,
AI_Adoption_Level (Low/Medium/High), Automation_Risk (Low/Medium/High),
Upskilling_Required (Yes/No), Job_Status (Replaced/Unchanged/...), Remote_Work (Yes/No)

Mixed dataset, with a slight majority of qualitative columns.

## Code

`ai_job_impact_analysis.ipynb` - the full analysis, with the written commentary
between the cells: loading, variable types, missing values, descriptive
statistics, feature engineering on the salary change, then five Plotly charts
(age distribution by AI adoption level, salaries before and after by job status,
experience against productivity, correlation heatmap, impact by industry and
risk level). The last cell builds an interactive Dash dashboard.

## Other files

- `1.png`, `2.png` - screenshots of the dashboard

## How to run

Open the notebook from inside this folder:

```
jupyter notebook ai_job_impact_analysis.ipynb
```

Requires pandas, numpy, plotly and dash.

The charts are Plotly figures. They are interactive in Jupyter and in VS Code,
but GitHub's notebook viewer does not run JavaScript, so on GitHub they show up
blank. Use nbviewer for a rendered view, or install kaleido and re-run to store
static images alongside them.

The last cell starts the Dash server and embeds it as an iframe in the notebook.
The port is not hardcoded: `port_libre()` scans upwards from 8050 and takes the
first free one. That matters because the iframe points at a plain
`http://127.0.0.1:<port>` address, so if another Dash application is already
listening on 8050 the notebook would display that other application instead of
this one. The printed line tells you which port was actually used.

The iframe is live only while the kernel is running. Reopening a saved notebook
shows an empty frame until you run the cell again.
