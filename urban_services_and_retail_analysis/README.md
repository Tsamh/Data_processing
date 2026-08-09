# Urban Services and Retail

## Datasets

- `airbnb_exam_dataset.csv` - 220 short term rental listings
- `taxi_trips_exam_dataset.csv` - 300 taxi trips
- `supermarket_sales_exam_dataset.csv` - 260 supermarket invoices

## Variable types

### airbnb_exam_dataset.csv (220 rows, 8 columns)
**Quantitative:** price, minimum_nights, number_of_reviews, availability_365, reviews_per_month
**Qualitative:** listing_id (identifier), neighbourhood, room_type

### taxi_trips_exam_dataset.csv (300 rows, 9 columns)
**Quantitative:** distance_km, duration_min, fare_amount, tip_amount, passenger_count
**Qualitative:** trip_id (identifier), pickup_zone, dropoff_zone, payment_type

### supermarket_sales_exam_dataset.csv (260 rows, 8 columns)
**Quantitative:** unit_price, quantity, total
**Qualitative:** invoice_id (identifier), city, product_category, customer_type, payment

All three are mixed, with quantitative measures broken down by a few categorical keys.

## Code

`airbnb_taxi_supermarket_analysis.ipynb` - loads the three files and runs the same
routine on each: inspection (Q1 to Q8) then manipulation and visualisation
(Q9 to Q34), with the written answers in markdown between the cells.

## Other files

`report_assets/` - the six figures used in the report. They were exported by hand,
the notebook does not write them, so re-running it leaves them untouched:

- `airbnb_hist_prix.png`, `airbnb_bar_quartier.png`
- `taxi_hist_duree.png`, `taxi_scatter_distance_prix.png`
- `supermarket_hist_total.png`, `supermarket_bar_categorie.png`

## How to run

Open the notebook from inside this folder. The three CSV files are read with
relative paths, so no change is needed:

```
jupyter notebook airbnb_taxi_supermarket_analysis.ipynb
```

Requires pandas, numpy and matplotlib.
