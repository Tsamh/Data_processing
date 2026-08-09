# data_processing

Each folder holds one body of work: the dataset it uses, the code that reads it,
a short readme, and the images or generated files.

Datasets are copied, never moved. When several pieces of code read the same file,
each one gets its own copy so the folders stay independent. Every code file is
named after the dataset it reads plus what sets that version apart from the
others.

Every notebook here has been run end to end from inside its own folder, so the
relative paths resolve, nothing raises, and the results and figures are already
stored in the file: you can read them without running anything. Two folders had
no code at all (Titanic, CO2), so an analysis notebook was written for each.

## Contents

| Folder | Subject | Data type |
|---|---|---|
| ai_employment_impact | AI impact on jobs, notebook and Dash dashboard | Mixed |
| covid19_worldwide_cases_analysis | COVID-19 daily counts by country | Mixed |
| stroke_risk_healthcare | Stroke screening, raw file | Mostly qualitative |
| stroke_risk_cleaning | Stroke screening, cleaning and analysis | Mostly qualitative |
| diabetes_and_stroke_screening | Diabetes and stroke, two files, one notebook | Quantitative and mixed |
| customer_anomaly_detection | Customer profiles, outlier detection | Mostly quantitative |
| student_academic_performance | Student scores and absences | Mostly quantitative |
| urban_services_and_retail_analysis | Airbnb, taxi and supermarket files | Mixed |
| titanic_passenger_survival | Titanic passengers, survival analysis | Mostly qualitative |
| co2_emissions_by_country | CO2 per capita by country and year | Mostly qualitative |
