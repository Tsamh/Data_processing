# CO2 Emissions by Country

## Dataset

`join_CO2_geography.csv` - per capita CO2 emissions by country and year, joined
with a geography reference table (region groupings, World Bank income class,
coordinates). 10512 usable rows, 13 columns, 191 countries, 1960 to 2014.

The file is a damaged export and needs care before anything else:

- the separator is a tab, not a comma
- decimal numbers use a comma (for example `0,0461`)
- the last column carries trailing commas left over from the export
- the encoding changes halfway through the file: the first 199 rows are plain
  text, everything after that is UTF-16LE

That last point is the dangerous one. `pd.read_csv` does not fail on it, it just
silently returns 199 rows out of 10512. The `charger()` function in the notebook
splits the file at the encoding break, decodes each half with the right codec and
reassembles it.

## Variable types

**Quantitative:** Annee (year), CO2 par habitant, Latitude, Longitude

**Qualitative:** country, Eight Regions, Four Regions, Geo (country code),
Members Oecd G77, Six Regions, UN member since,
World bank income group 2017, World bank region

Mostly qualitative: one real measure (CO2 per capita) described by a long list of
geographic and political groupings.

## Code

`join_co2_geography_emissions_analysis.ipynb` - written for this folder, since no
analysis code for this file existed in the source folders. It covers:

1. Loading and repairing the file
2. Inspection and data quality
3. Univariate analysis of the emissions variable, raw and on a log scale
4. Evolution over time, mean against median
5. Comparison by World Bank income group and by broad region
6. Highest and lowest emitters per capita over 2005 to 2014
7. Geographic scatter using the latitude and longitude columns
8. Export of a clean file

## Other files

- `co2_par_habitant_propre.csv` - the repaired table written by the notebook:
  UTF-8, comma separated, dot as decimal separator. Ready for pandas, Excel or
  Tableau without any of the workarounds above.

## How to run

```
jupyter notebook join_co2_geography_emissions_analysis.ipynb
```

Requires pandas, numpy, matplotlib and seaborn. Run it from inside this folder so
the relative paths resolve. Re-running it overwrites `co2_par_habitant_propre.csv`.
