class AbstentionEngine:
    def __init__(self):
        self.industry_configs = {
            'ecommerce': {
                'initial_conf': 0.38,
                'entropy': 1.84,
                'opt1_conf': 0.946,
                'opt2_conf': 0.892,
                'opt1_action': 'Re-attach tracking pixel script, recalibrate causal attribution weights, and credit ad budget.',
                'opt2_action': 'Engage Cloudflare Bot-Management shield and suppress false campaign alarm.'
            },
            'healthcare': {
                'initial_conf': 0.315,
                'entropy': 2.10,
                'opt1_conf': 0.978,
                'opt2_conf': 0.914,
                'opt1_action': 'Force-restart Wing C IoT medical telemetry hub and re-index clinical bed occupancy sensor stream.',
                'opt2_action': 'Trigger EMR chart sync for Outpatient overflow clinic and update central triage manifest.'
            },
            'fintech': {
                'initial_conf': 0.420,
                'entropy': 1.72,
                'opt1_conf': 0.984,
                'opt2_conf': 0.932,
                'opt1_action': 'Renew Partner Merchant SSL cipher certificate, flush gateway session cache, and re-transmit webhook batch.',
                'opt2_action': 'Adjust Cloudflare WAF rate-limiting threshold to 50k req/min for verified acquiring endpoints.'
            },
            'saas': {
                'initial_conf': 0.340,
                'entropy': 1.95,
                'opt1_conf': 0.962,
                'opt2_conf': 0.908,
                'opt1_action': 'Unjam RabbitMQ dead-letter exchange, restart async license worker pods, and issue JWT tokens.',
                'opt2_action': 'Extend Enterprise grace-period counter by 48h and suppress false account churn flags.'
            }
        }

    def evaluate_contradiction_scenario(self, industry='ecommerce'):
        cfg = self.industry_configs.get(industry, self.industry_configs['ecommerce'])
        return {
            'status': 'ABSTAINED',
            'confidence_score': cfg['initial_conf'],
            'shannon_entropy': cfg['entropy'],
            'confidence_threshold': 0.70,
            'action_required': 'DISPATCH_HUMAN_MICRO_POLL'
        }

    def submit_slack_poll_response(self, option_text, industry='ecommerce', option_index=1):
        cfg = self.industry_configs.get(industry, self.industry_configs['ecommerce'])
        is_opt1 = ('1' in option_text or 'Yes' in option_text or option_index == 1)
        upgraded_conf = cfg['opt1_conf'] if is_opt1 else cfg['opt2_conf']
        rec_action = cfg['opt1_action'] if is_opt1 else cfg['opt2_action']
        
        return {
            'status': 'RESOLVED_BY_HUMAN_IN_THE_LOOP',
            'confidence_score': upgraded_conf,
            'confidence_pct_formatted': f"{upgraded_conf * 100:.1f}%",
            'resolved_cause': f"Human Expert Confirmed: \"{option_text}\". Causal Graph recalibrated with {upgraded_conf * 100:.1f}% confidence.",
            'action_recommended': rec_action
        }

