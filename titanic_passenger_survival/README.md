# Titanic Passenger Survival

## Dataset

`titanic_data.csv` - 891 passengers, 12 columns. The classic Titanic training set.
`Age` has missing values and `Cabin` is missing for most rows.

## Variable types

**Quantitative:** Age, SibSp (siblings and spouses aboard), Parch (parents and
children aboard), Fare

**Qualitative:** PassengerId (identifier), Name, Sex, Ticket, Cabin, Embarked,
plus Pclass and Survived, which are numeric but categorical in meaning
(1/2/3 class, 0/1 survival)

Mixed dataset, leaning qualitative once Pclass and Survived are counted as categories.

## Code

`titanic_data_survival_analysis.ipynb` - written for this folder, since no analysis
code for the Titanic file existed in the source folders. It covers:

1. Loading and inspection
2. Data quality and cleaning (age imputed by sex and class, port filled with the
   mode, cabin reduced to a "known / unknown" flag)
3. Univariate analysis of age, fare, sex, class and port
4. Survival rate by sex, class, age band, fare quartile and cabin flag, with a
   sex-by-class heatmap
5. Correlation matrix
6. Written summary

## How to run

```
jupyter notebook titanic_data_survival_analysis.ipynb
```

Requires pandas, numpy, matplotlib and seaborn. The notebook writes nothing to
disk and reads the CSV with a relative path, so run it from inside this folder.
