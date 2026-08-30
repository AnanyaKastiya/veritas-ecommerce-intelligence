import json
import numpy as np
import pandas as pd

class AnomalyDetector:
    def __init__(self, orders_file='data/orders_hourly.json'):
        with open(orders_file, 'r', encoding='utf-8') as f:
            self.orders = json.load(f)
        self.df = pd.DataFrame(self.orders)

    def analyze_latest_window(self, window_hours=8):
        df_sorted = self.df.sort_values('timestamp')
        historical = df_sorted.iloc[:-window_hours]
        latest = df_sorted.iloc[-window_hours:]

        # Filter historical data for matching evening hours (16:00 - 23:00)
        historical['dt'] = pd.to_datetime(historical['timestamp'])
        historical_peak = historical[historical['dt'].dt.hour >= 16]
        
        baseline_gmv_mean = float(historical_peak['gmv'].mean())
        baseline_gmv_std = float(historical_peak['gmv'].std()) if float(historical_peak['gmv'].std()) > 0 else 3500.0
        
        current_gmv = float(latest['gmv'].sum())
        expected_gmv = float(baseline_gmv_mean * window_hours)
        
        gmv_delta_usd = current_gmv - expected_gmv
        gmv_delta_pct = (gmv_delta_usd / expected_gmv) * 100

        current_sla_breach = float(latest['delivery_sla_breach_rate'].mean())
        baseline_sla_breach = float(historical['delivery_sla_breach_rate'].mean())

        # Z-score against matching peak window
        hourly_delta = abs(gmv_delta_usd / window_hours)
        z_score = hourly_delta / baseline_gmv_std
        is_statistically_significant = bool(z_score > 1.8 or abs(gmv_delta_pct) > 10.0)
        is_financially_material = bool(abs(gmv_delta_usd) >= 10000.0)

        is_material_anomaly = bool(is_statistically_significant and is_financially_material)
        surprise_entropy = min(1.0, round(float(z_score / 3.0), 3))

        return {
            'window_hours': window_hours,
            'is_material_anomaly': is_material_anomaly,
            'metric_id': 'kpi_gmv',
            'metric_name': 'Gross Merchandise Value (GMV)',
            'current_gmv_usd': round(current_gmv, 2),
            'expected_baseline_usd': round(expected_gmv, 2),
            'gmv_delta_usd': round(gmv_delta_usd, 2),
            'gmv_delta_pct': round(gmv_delta_pct, 2),
            'z_score': round(float(z_score), 2),
            'surprise_entropy_score': surprise_entropy,
            'current_delivery_sla_breach_pct': round(current_sla_breach, 2),
            'baseline_delivery_sla_breach_pct': round(baseline_sla_breach, 2),
            'materiality_evaluation': {
                'statistical_significance': is_statistically_significant,
                'dollar_threshold_exceeded': is_financially_material,
                'threshold_rule': 'Delta >= ,000 USD and (Z-score > 1.8 or Drop > 10%)'
            }
        }
