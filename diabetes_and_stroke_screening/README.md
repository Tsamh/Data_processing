# Diabetes and Stroke Screening

## Datasets

This folder holds two files because the notebook analyses both, one after the other.

`diabetes_dataset (1).csv` - 768 patients, 9 columns (Pima Indians diabetes data).
`dataset_stroke_nouv.csv` - 5110 patients, 12 columns.

## Variable types

### diabetes_dataset (1).csv
**Quantitative:** Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
BMI, DiabetesPedigreeFunction, Age
**Qualitative:** Outcome, coded 0/1 but categorical in meaning

Fully quantitative apart from the target. Note that several columns use 0 as a
placeholder for a missing measurement.

### dataset_stroke_nouv.csv
**Quantitative:** age, avg_glucose_level, bmi
**Qualitative:** gender, ever_married, work_type, Residence_type, smoking_status,
and the 0/1 flags hypertension, heart_disease, stroke

Mostly qualitative with three continuous clinical measures.

## Code

`diabetes_and_stroke_side_by_side.ipynb` - loads the diabetes file first, then the stroke file, and runs the
same exploratory routine on both so the two can be compared.

## How to run

```
jupyter notebook diabetes_and_stroke_side_by_side.ipynb
```

Requires pandas, numpy, matplotlib and seaborn.
