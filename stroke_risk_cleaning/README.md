# Stroke Risk - Cleaning and Analysis

## Dataset

`dataset_stroke_nouv.csv` - 5110 patients, 12 columns. Reworked version of the
stroke file used for the data cleaning exercise, with missing values in `bmi`,
`avg_glucose_level` and `smoking_status`.

## Variable types

**Quantitative:** age, avg_glucose_level, bmi

**Qualitative:** gender, ever_married, work_type, Residence_type, smoking_status,
plus the binary flags hypertension, heart_disease and stroke, which are coded 0/1
but are categorical in meaning

Mostly qualitative dataset with three continuous clinical measures.

## Code

`stroke_dataset_cleaning_and_analysis.ipynb` - complete exploratory analysis in
six parts: inspection, identification of the problems, preparation, treatment of
the missing values by mean and mode imputation, then univariate and bivariate
analysis before and after treatment, with the written answers in markdown.
Imputing rather than dropping keeps all 5110 rows, so the before and after
distributions are compared on the same population.

## How to run

```
jupyter notebook "stroke_dataset_cleaning_and_analysis.ipynb"
```

Requires pandas, numpy, matplotlib and seaborn.
