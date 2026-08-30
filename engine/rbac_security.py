class RBACSecurityEngine:
    def apply_security_masking(self, persona, payload):
        sanitized = dict(payload)
        if persona == 'operations_lead':
            if 'gross_margin_usd' in sanitized:
                sanitized['gross_margin_usd'] = 'LOCKED (RESTRICTED: C-LEVEL ONLY)'
            if 'executive_bonus_pool' in sanitized:
                sanitized['executive_bonus_pool'] = 'LOCKED (RESTRICTED)'
            sanitized['security_tier_active'] = 'OPEN_ENTERPRISE'
        else:
            sanitized['security_tier_active'] = 'CONFIDENTIAL_FINANCIAL_FULL_ACCESS'
        return sanitized
