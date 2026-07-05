<<<<<<< HEAD
<<<<<<< HEAD
# Hotel Revenue & Occupancy Forecasting

**Objective:** Predict future room occupancy and revenue trends from historical
booking data, identify peak demand seasons, and recommend a dynamic pricing
strategy to maximize TRevPAR (Total Revenue Per Available Room).

**Tools:** Python (Pandas, NumPy, Scikit-learn, Matplotlib)

## What the script does
1. **Generates 2 years of synthetic daily booking data** (150-room property)
   with realistic seasonality (winter + summer peaks), weekend demand spikes,
   and a mild growth trend — `hotel_bookings_2023_2024.csv`.
2. **Identifies peak vs. standard demand months** using a quantile threshold
   on monthly occupancy — `outputs/monthly_summary.csv`.
3. **Trains a Random Forest regression model** to forecast occupancy rate
   from calendar features (month, weekday, weekend flag, season flag).
   Achieved **R² ≈ 0.83** on held-out data.
4. **Forecasts Q1 2025 occupancy** and applies a **rule-based dynamic pricing
   engine**: rates flex from -15% (low demand) to +35% (high demand) versus
   a flat baseline rate.
5. **Quantifies the pricing strategy's impact**: dynamic pricing projects
   roughly a **16-17% revenue lift** over flat pricing for the same forecast
   period.

## Files
| File | Description |
|---|---|
| `hotel_bookings_2023_2024.csv` | Raw synthetic historical data |
| `outputs/monthly_summary.csv` | Monthly occupancy/revenue/RevPAR + demand label |
| `outputs/forecast_2025_q1_with_pricing.csv` | Forecast + recommended rate/action per day |
| `outputs/01_monthly_occupancy_revpar.png` | Occupancy vs RevPAR trend |
| `outputs/02_peak_vs_standard_revenue.png` | Revenue share: peak vs standard months |
| `outputs/03_actual_vs_predicted.png` | Model accuracy plot |
| `outputs/04_q1_2025_forecast_pricing.png` | Forecast colored by pricing action |

## How to run
```bash
python3 revenue_forecasting.py
```

## Note on the data
This is **synthetic data generated for demonstration purposes** — built to
show the full analytical workflow (data → model → business recommendation)
since no real hotel dataset was available. If you have access to real PMS
(Opera/Marsha) export data, swap the `generate_data()` step for a CSV import
and the rest of the pipeline runs unchanged.
=======
# hotel-revenue-forecaster
>>>>>>> 58a4fa043525b3679dd262a20a913988a98dbc7b
=======
# hotel-revenue-forecaster
>>>>>>> 46cf2c326351d31b161785600f130f8c3e5e69e7
