import json
import csv
import random
import datetime
import pandas as pd
import numpy as np

def generate_datasets():
    print('Generating heterogeneous multi-source datasets...')
    
    # 1. Hourly Transactional Orders (Hourly SQL Data) - 14 Days of Hourly Data
    timestamps = []
    base_time = datetime.datetime(2026, 8, 14, 0, 0, 0)
    rows = []
    
    # Simulate normal days, then Friday Aug 28 Anomaly
    for hour_idx in range(14 * 24):
        curr_time = base_time + datetime.timedelta(hours=hour_idx)
        hour = curr_time.hour
        day_of_week = curr_time.weekday() # 4 is Friday
        
        # Base volume seasonality (peaks in evening 18:00 - 21:00)
        base_vol = 1200 + 600 * np.sin((hour - 8) / 24 * 2 * np.pi) + (300 if day_of_week in [4, 5] else 0)
        base_aov = 34.50 + random.uniform(-1.5, 1.5)
        sla_breach = random.uniform(3.0, 6.5) # normal 4-6%
        
        # Inject Multi-Factor Anomaly on the final Friday evening (hours 328-335)
        is_anomaly_window = (hour_idx >= (14 * 24 - 8))
        if is_anomaly_window:
            # Drop volume by 14%, spike SLA breach to 28.4%, slight AOV increase
            vol = int(base_vol * 0.86)
            aov = base_aov * 1.02 # .20
            sla_breach = 28.4
            gmv = vol * aov
            status = 'ANOMALY_LOGISTICS_STRIKE'
        else:
            vol = int(base_vol + random.uniform(-50, 50))
            aov = base_aov
            gmv = vol * aov
            status = 'NORMAL'
            
        rows.append({
            'timestamp': curr_time.isoformat(),
            'region': 'Southwest_Dallas',
            'order_volume': vol,
            'aov': round(aov, 2),
            'gmv': round(gmv, 2),
            'delivery_sla_breach_rate': round(sla_breach, 2),
            'gross_margin_usd': round(gmv * 0.285, 2),
            'status': status
        })
        
    df_orders = pd.DataFrame(rows)
    df_orders.to_json('data/orders_hourly.json', orient='records', indent=2)
    df_orders.to_csv('data/orders_hourly.csv', index=False)
    print(f'Generated {len(df_orders)} hourly order records in data/orders_hourly.json and .csv')

    # 2. Daily Unstructured Customer Support Tickets (Zendesk CRM API)
    tickets = [
        {
            'ticket_id': 'ZD-98121',
            'timestamp': '2026-08-28T18:45:00Z',
            'region': 'Southwest_Dallas',
            'category': 'Late Delivery',
            'sentiment': 'Negative (-0.88)',
            'text': 'My dinner order took 85 minutes to arrive! The courier driver said there was a strike at the Dallas transit hub. Food was ice cold. I want an immediate full refund.',
            'refund_requested': True,
            'refund_amount_usd': 42.50
        },
        {
            'ticket_id': 'ZD-98144',
            'timestamp': '2026-08-28T19:12:00Z',
            'region': 'Southwest_Dallas',
            'category': 'Order Cancellation',
            'sentiment': 'Negative (-0.94)',
            'text': 'App showed delivery in 20 mins, now it says delayed by 60 mins. Cancelled order and ordering from QuickMart instead who has a 15% discount promo active.',
            'refund_requested': True,
            'refund_amount_usd': 38.00
        },
        {
            'ticket_id': 'ZD-98189',
            'timestamp': '2026-08-28T19:50:00Z',
            'region': 'Southwest_Dallas',
            'category': 'Courier Unavailability',
            'sentiment': 'Negative (-0.79)',
            'text': 'Unable to find available delivery partner for 30 minutes in North Dallas. App kept searching then timed out.',
            'refund_requested': False,
            'refund_amount_usd': 0.0
        },
        {
            'ticket_id': 'ZD-98210',
            'timestamp': '2026-08-28T20:15:00Z',
            'region': 'Southwest_Dallas',
            'category': 'App Interface / Checkout',
            'sentiment': 'Neutral (-0.12)',
            'text': 'Payment went through quickly, but tracking screen froze on Dispatching stage.',
            'refund_requested': False,
            'refund_amount_usd': 0.0
        }
    ]
    with open('data/support_tickets_daily.json', 'w', encoding='utf-8') as f:
        json.dump(tickets, f, indent=2)
    print(f'Generated {len(tickets)} support ticket records in data/support_tickets_daily.json')

    # 3. Weekly Competitor Web Scraping Feed (External Intelligence)
    competitor_data = [
        {'competitor_name': 'QuickMart Express', 'region': 'Southwest_Dallas', 'discount_depth_pct': 15.0, 'campaign_name': 'Weekend Rush Flash Sale', 'active_since': '2026-08-28T16:00:00Z', 'app_rank': 2},
        {'competitor_name': 'InstaFast', 'region': 'Southwest_Dallas', 'discount_depth_pct': 0.0, 'campaign_name': 'Standard Pricing', 'active_since': '2026-08-01T00:00:00Z', 'app_rank': 4},
        {'competitor_name': 'BlinkBasket', 'region': 'Southwest_Dallas', 'discount_depth_pct': 5.0, 'campaign_name': 'Friday Snacks Bundle', 'active_since': '2026-08-28T12:00:00Z', 'app_rank': 3}
    ]
    with open('data/competitor_prices_weekly.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=competitor_data[0].keys())
        writer.writeheader()
        writer.writerows(competitor_data)
    print('Generated data/competitor_prices_weekly.csv')

    # 4. Sparse History / Cold-Start Data (Austin Launch Hub - 72 Hours Old)
    cold_start_data = {
        'hub_id': 'HUB_TX_AUSTIN_01',
        'hub_name': 'Austin Central Ultra-Fast Hub',
        'launch_date': '2026-08-25T08:00:00Z',
        'hours_live': 72,
        'current_metrics': {
            'day_3_gmv_usd': 14850.0,
            'day_1_gmv_usd': 18200.0,
            'day_3_change_pct': -18.4,
            'order_count': 420,
            'delivery_sla_breach_rate': 5.2
        },
        'historical_peer_cohorts': {
            'dallas_launch_day_3_change_pct': -19.2,
            'houston_launch_day_3_change_pct': -17.8,
            'cohort_median_day_3_change_pct': -18.5,
            'status': 'HEALTHY_ON_BENCHMARK'
        }
    }
    with open('data/historical_launches.json', 'w', encoding='utf-8') as f:
        json.dump(cold_start_data, f, indent=2)
    print('Generated data/historical_launches.json (Cold Start scenario)')

    # 5. Closed-Loop Action Efficacy Tracking Store (Option 3B Learning Store)
    efficacy_store = [
        {
            'action_id': 'ACT-2026-0801',
            'timestamp': '2026-08-01T14:30:00Z',
            'playbook_name': 'Emergency 3PL Courier Fleet Failover',
            'driver_addressed': 'Courier Partner Capacity Bottleneck',
            'approved_by': 'Chief Commercial Officer',
            'cost_incurred_usd': 12000.0,
            'projected_recovery_usd': 45000.0,
            'realized_recovery_usd': 42500.0,
            'realization_accuracy_pct': 94.4,
            'status': 'RESOLVED_VERIFIED',
            'playbook_trust_level': 'TIER_1_HIGH_CONFIDENCE'
        },
        {
            'action_id': 'ACT-2026-0810',
            'timestamp': '2026-08-10T10:15:00Z',
            'playbook_name': 'Targeted Customer Goodwill Credit ( Rebate)',
            'driver_addressed': 'Customer Ticket Surge & Negative Sentiment',
            'approved_by': 'VP of Customer Experience',
            'cost_incurred_usd': 8500.0,
            'projected_recovery_usd': 28000.0,
            'realized_recovery_usd': 26900.0,
            'realization_accuracy_pct': 96.1,
            'status': 'RESOLVED_VERIFIED',
            'playbook_trust_level': 'TIER_1_HIGH_CONFIDENCE'
        },
        {
            'action_id': 'ACT-2026-0818',
            'timestamp': '2026-08-18T16:00:00Z',
            'playbook_name': 'Flash Price Match Discount (5% Counter-Promo)',
            'driver_addressed': 'Competitor Flash Campaign Displacement',
            'approved_by': 'Pricing Director',
            'cost_incurred_usd': 15000.0,
            'projected_recovery_usd': 35000.0,
            'realized_recovery_usd': 31200.0,
            'realization_accuracy_pct': 89.1,
            'status': 'RESOLVED_VERIFIED',
            'playbook_trust_level': 'TIER_2_MODERATE_CONFIDENCE'
        }
    ]
    with open('data/feedback_audit_store.json', 'w', encoding='utf-8') as f:
        json.dump(efficacy_store, f, indent=2)
    print('Generated data/feedback_audit_store.json (Action Efficacy & Learning Store)')

if __name__ == '__main__':
    generate_datasets()
