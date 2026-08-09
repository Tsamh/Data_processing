# Stroke Risk - Healthcare Screening

## Dataset

`healthcare-dataset-stroke-data.csv` - 5110 patients, 12 columns. The original
Kaggle stroke file, before any cleaning. Note that `bmi` still contains the
literal string "N/A" in this version, which is why it reads as text.

## Variable types

**Quantitative:** age, avg_glucose_level, bmi (once the "N/A" values are converted)

**Qualitative:** gender, ever_married, work_type, Residence_type, smoking_status,
plus hypertension, heart_disease and stroke, which are 0/1 flags and categorical
in meaning

Mostly qualitative dataset with three continuous clinical measures.

## Code

`healthcare_stroke_data_first_inspection.ipynb` - first pass over the data:
structure, types, missing values and a first look at how stroke relates to age
and glucose level.

## How to run

```
jupyter notebook healthcare_stroke_data_first_inspection.ipynb
```

Requires pandas, numpy, matplotlib and seaborn.
