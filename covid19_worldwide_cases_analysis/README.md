# COVID-19 Worldwide Cases

## Dataset

`covid_19_data.csv` - 4247 rows, 8 columns. Daily cumulative counts per province
or region, from 22 January 2020 to 8 March 2020, covering 111 countries or regions.

## Variable types

**Quantitative:** SNo (row id), Confirmed, Deaths, Recovered

**Qualitative:** ObservationDate, Province/State, Country/Region, Last Update
(the two date columns are stored as text and need parsing)

Mixed dataset: 3 real quantitative measures observed across qualitative
geographic and time dimensions.

## Code

`covid_19_data_country_comparison.ipynb` - inspection, date parsing, missing value
treatment, outlier detection with a MAD rule (globally and per country), a
consistency check on deaths against confirmed cases, then the country level
comparison and the time series of confirmed, deaths and recovered.

## Other files

- `interpretation_covid19.md` - written interpretation of the analysis

## How to run

```
jupyter notebook covid_19_data_country_comparison.ipynb
```

Requires pandas, numpy, matplotlib and seaborn.
