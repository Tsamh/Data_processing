# Student Academic Performance

## Datasets

`EduStats_Students (2) (2).csv` - 2000 students, 16 columns. Raw file, with
inconsistent category labels (for example "female" and "F", "DAKAR" and "Dakar")
and missing values in HoursStudyPerWeek.

`Students_cleaned.csv` - same 2000 students after the notebook has normalised the
labels and encoded InternetAccess as 0/1. This is the notebook's output.

## Variable types

**Quantitative:** Age, HoursStudyPerWeek, HouseholdIncome, MathScore,
ReadingScore, WritingScore, Abs_Jan, Abs_Feb, Abs_Mar, TotalAbsences

**Qualitative:** StudentID (identifier), Gender, ParentalEducation, Region,
InternetAccess, PassFail (0/1 but categorical in meaning)

Mixed dataset, leaning quantitative: 10 real numeric measures against 4 categories
plus two binary flags.

## Code

`edustats_students_cleaning_and_analysis.ipynb` - inspection, label normalisation, missing value treatment, then
analysis of scores against study hours, absences and parental education. The last
cell writes `Students_cleaned.csv`.

## How to run

```
jupyter notebook edustats_students_cleaning_and_analysis.ipynb
```

Requires pandas, numpy, matplotlib and seaborn.
