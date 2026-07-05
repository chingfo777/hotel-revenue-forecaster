import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

RNG = np.random.default_rng(42)
TOTAL_ROOMS = 150


def run_forecasting_pipeline(file_path=None, df_input=None):
    # 1. LOAD DATA SOURCE
    if df_input is not None:
        df = df_input.copy()
    elif file_path:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
    else:
        # Fallback to internal generation if everything else is empty
        return None

    # FIX: Force clean lowercase columns to match your original processing script logic
    df.columns = df.columns.str.strip().str.lower()

    # Ensure correct datetime parsing
    df['date'] = pd.to_datetime(df['date'])

    # 2. MONTHLY AGGREGATIONS
    df['month_str'] = df['date'].dt.strftime('%Y-%m')
    monthly = df.groupby('month_str').agg(
        avg_occupancy=("occupancy_rate", "mean"),
        total_revenue=("revenue", "sum"),
        avg_revpar=("revpar", "mean"),
    ).reset_index()

    peak_threshold = monthly["avg_occupancy"].quantile(0.65)
    monthly["demand_level"] = np.where(monthly["avg_occupancy"] >= peak_threshold, "Peak", "Standard")
    season_rev = monthly.groupby("demand_level")["total_revenue"].sum().to_dict()

    # 3. MACHINE LEARNING MODEL SUITE
    features = ["month", "day_of_week", "is_weekend", "is_peak_season"]
    X = df[features]
    y = df["occupancy_rate"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # 4. FORWARD PROJECTIONS (Q1 2025)
    future_dates = pd.date_range("2025-01-01", "2025-03-31", freq="D")
    future = pd.DataFrame({"date": future_dates})
    future["month"] = future["date"].dt.month
    future["day_of_week"] = future["date"].dt.dayofweek
    future["is_weekend"] = future["day_of_week"].isin([4, 5]).astype(int)
    future["is_peak_season"] = future["month"].isin({11, 12, 1, 2, 6, 7, 8}).astype(int)
    future["predicted_occupancy"] = model.predict(future[features]).clip(0.15, 0.98)

    def recommend_price(predicted_occupancy, base_rate=180):
        if predicted_occupancy >= 0.80:
            return round(base_rate * 1.35, 2), "Increase (+35%)"
        elif predicted_occupancy >= 0.65:
            return round(base_rate * 1.15, 2), "Increase (+15%)"
        elif predicted_occupancy >= 0.45:
            return round(base_rate * 1.00, 2), "Hold"
        else:
            return round(base_rate * 0.85, 2), "Discount (-15%)"

    future[['recommended_rate', 'pricing_action']] = future['predicted_occupancy'].apply(
        lambda p: pd.Series(recommend_price(p))
    )

    flat_revenue = (future["predicted_occupancy"] * TOTAL_ROOMS * 180).sum()
    dynamic_revenue = (future["predicted_occupancy"] * TOTAL_ROOMS * future["recommended_rate"]).sum()
    trevpar_lift_pct = (dynamic_revenue - flat_revenue) / flat_revenue * 100

    # 5. SECURE TRANSFORMATION TO NATIVE WEB TYPES
    payload = {
        "kpis": {
            "mae": float(round(mae, 4)),
            "r2": float(round(r2, 2)),
            "flat_rev": f"{flat_revenue:,.0f}",
            "dyn_rev": f"{dynamic_revenue:,.0f}",
            "lift": float(round(trevpar_lift_pct, 1))
        },
        "monthly_chart": {
            "labels": monthly["month_str"].tolist(),
            "occupancy": (monthly["avg_occupancy"] * 100).round(1).tolist(),
            "revpar": monthly["avg_revpar"].round(2).tolist()
        },
        "revenue_share": {
            "labels": [str(k) for k in season_rev.keys()],
            "values": [float(round(v, 2)) for v in season_rev.values()]
        },
        "model_fit": {
            "actual": [float(x) for x in y_test.round(3).tolist()[:150]],
            "predicted": [float(x) for x in y_pred.round(3).tolist()[:150]]
        },
        "forecast": {
            "labels": future["date"].dt.strftime('%Y-%m-%d').tolist(),
            "occupancy": (future["predicted_occupancy"] * 100).round(1).tolist(),
            "actions": future["pricing_action"].tolist()
        }
    }
    return payload