# Customer Profiles - Anomaly Detection

## Dataset

`dataset_anomalies.csv` - 2020 rows, 15 columns. Synthetic customer profiles with
deliberately injected outliers and missing values, used for the anomaly detection
exercise. Column names are in French.

## Variable types

**Quantitative:** Age, Revenu, IMC, Achats, Score_Credit, Nombre_Enfants,
Depenses_Mensuelles, Epargne, Temps_Travail, Satisfaction_Client,
Anciennete_Client, Score_Sante

**Qualitative:** Genre, Statut_Marital, Ville

Predominantly quantitative dataset (12 numeric columns out of 15).

## Code

`dataset_anomalies_cleaning_and_export.ipynb` - detection of missing values, hidden
missing values (empty strings, "NA", "?"), duplicates and outliers, then treatment
of each case variable by variable, and export of the corrected table.

## Other files

- `df_util_modif.csv` - the table written by the notebook, ready for Tableau

## How to run

```
jupyter notebook dataset_anomalies_cleaning_and_export.ipynb
```

Requires pandas, numpy, matplotlib and seaborn.
