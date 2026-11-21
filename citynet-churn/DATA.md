# Data card: CityNet customer records

## Training file

- File: `data/citynet_churn.csv`
- Source: Made-up CityNet customer records for this course.
- Rows: 5,000
- Columns: 14
- One row: one customer, measured over the last 90 days.
- Target: `churned = 1` if the customer cancelled in the next month.
- Target distribution: 4,104 retained (82.08%) and 896 churned (17.92%).

## Prediction file

- File: `data/new_customers.csv`
- Rows: 8
- Columns: 12
- This file contains new-customer records without the `cancel_request_logged` or `churned` columns.

## Columns

### Used as numeric features

- `monthly_bill`
- `tenure_months`
- `support_calls_90d`
- `outage_hours_90d`
- `age`

### Used as categorical features

- `region`
- `plan`
- `tv_bundle`
- `payment_method`
- `auto_pay`
- `paid_late_last_bill`

### Identifier

- `customer_id`: identifying information only; not used for prediction.

### Target

- `churned`: training label.

### Excluded leakage or risk column

- `cancel_request_logged`: it predicts churn almost perfectly because it directly reflects cancellation behavior. It must not be included as a normal input feature.

## Missing values

- `payment_method`: 149 missing values.
- `age`: 411 missing values.
- Numeric missing values should be median-imputed.
- Categorical missing values should be most-frequent-imputed.

## Known issues and limitations

- Synthetic course data may not reflect real customer behavior or data quality.
- Churn is imbalanced, so accuracy alone is not an adequate metric.
- `cancel_request_logged` is target leakage and must remain excluded.
- The split must use stratification to preserve the observed 17.92% churn rate across subsets.
- Customer identifiers must not become model features.
- Missing-value imputers should be fitted on training data only.
