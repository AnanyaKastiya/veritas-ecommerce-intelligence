class NarrativeGenerator:
    def generate_persona_narrative(self, persona, anomaly_data, driver_data, tribunal_data):
        gmv_drop = abs(anomaly_data['gmv_delta_usd'])
        gmv_pct = abs(anomaly_data['gmv_delta_pct'])
        sla_breach = anomaly_data['current_delivery_sla_breach_pct']

        if persona == 'executive_vp':
            return {
                'persona': 'executive_vp',
                'title': 'Executive Commercial Briefing: Southwest Dallas GMV Drop',
                'executive_summary': (
                    'Southwest Dallas revenue declined by $' + f'{gmv_drop:,.2f}' + ' (-' + str(gmv_pct) + '%) during Friday peak hours. '
                    'Our Causal Tribunal identified a primary operational driver (Dallas courier hub capacity shortage causing ' + str(sla_breach) + '% late deliveries) '
                    'interacting with an aggressive 15% flash discount launched by competitor QuickMart. '
                    'Estimated gross margin erosion is ,070 USD.'
                ),
                'strategic_implications': [
                    'Immediate customer goodwill erosion: 42 high-sentiment refund tickets escalated in Zendesk.',
                    'Market share capture by QuickMart: Dallas regional app store rank shifted from #4 to #2.',
                    'Zero data pipeline integrity issues detected (PostgreSQL & Stripe webhooks verified).'
                ],
                'recommended_executive_action': {
                    'action_title': 'Authorize ,000 Emergency 3PL Fleet Failover +  Customer Goodwill Rebates',
                    'cost_usd': 15000.0,
                    'projected_recovery_usd': 42000.0,
                    'net_roi_usd': 27000.0,
                    'decision_right_required': 'AUTHORIZE_CUSTOMER_REBATES_UPTO_50K',
                    'monitoring_plan': '7-day automated closed-loop recovery tracking via Action Efficacy Store.'
                }
            }
        else:
            return {
                'persona': 'operations_lead',
                'title': 'Regional Logistics Operational Diagnostic: Dallas Hub Backlog',
                'operational_summary': (
                    'Dallas Southwest Hub experienced an operational SLA breach of ' + str(sla_breach) + '% (Baseline: 4.8%). '
                    'Fulfillment latency rose from 18 mins to 82 mins due to courier driver unavailability. '
                    'Order cancellations surged across 42 delivery routes.'
                ),
                'tactical_breakdown': [
                    'Warehouse fulfillment backlog: Dallas Hub #42 queue peaked at 380 unassigned orders.',
                    'Customer sentiment: 88% of Zendesk tickets cite cold food and 60+ min courier delay.',
                    'Financial profit margins: [LOCKED - RESTRICTED TO C-LEVEL & VP ROLES]'
                ],
                'recommended_tactical_action': {
                    'action_title': 'Reroute 40% of Dallas Hub Traffic to North Backup Hub & Trigger Driver Overtime',
                    'cost_usd': 4500.0,
                    'projected_sla_recovery': 'Reduce late delivery rate back to 6.2% within 90 minutes',
                    'decision_right_required': 'REROUTE_ORDERS_TO_BACKUP_3PL',
                    'monitoring_plan': 'Real-time Kafka 5-min dispatch stream monitoring.'
                }
            }
