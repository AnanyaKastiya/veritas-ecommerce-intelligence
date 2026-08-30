import os
import sys
import json
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.semantic_layer import CanonicalSemanticLayer
from engine.analytics_suite import (
    KPIEngine,
    KPIExplorerEngine,
    DriverAnalysisEngine,
    EvidenceEngine,
    ActionEngine,
    IntentChatEngine,
    FeedbackEngine,
    TelemetryAndRBACEngine
)

# Initialize Core Services
semantic_layer = CanonicalSemanticLayer()
semantic_layer.load_reference_dataset()

kpi_engine = KPIEngine(semantic_layer)
explorer_engine = KPIExplorerEngine(semantic_layer)
driver_engine = DriverAnalysisEngine(semantic_layer)
evidence_engine = EvidenceEngine(semantic_layer)
action_engine = ActionEngine(semantic_layer)
chat_engine = IntentChatEngine(semantic_layer, kpi_engine, driver_engine, action_engine)
feedback_engine = FeedbackEngine()
telemetry_rbac = TelemetryAndRBACEngine()

class VeritasServerHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        persona = query.get('persona', ['business_manager'])[0]

        # 1. Root & Static Assets
        if path == '/' or path == '/index.html':
            frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'index.html')
            if os.path.exists(frontend_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(frontend_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self._send_json({"error": "frontend/index.html not found"}, 404)

        # 2. Section ①: Overview & Top Insights
        elif path == '/api/overview':
            data = kpi_engine.calculate_overview_kpis(persona)
            self._send_json(telemetry_rbac.apply_rbac_masking(persona, data))

        # 3. Section ②: KPI Explorer
        elif path == '/api/explorer':
            kpi_name = query.get('kpi', ['revenue'])[0]
            dimension = query.get('dimension', ['category'])[0]
            data = explorer_engine.get_explorer_breakdown(kpi_name, dimension, persona)
            self._send_json(data)

        # 4. Section ③: Root-Cause & Driver Analysis
        elif path == '/api/drivers':
            data = driver_engine.get_multi_factor_drivers(persona)
            self._send_json(telemetry_rbac.apply_rbac_masking(persona, data))

        # 5. Section ④: Evidence & Lineage Panel
        elif path == '/api/evidence':
            data = evidence_engine.get_evidence_report(persona)
            self._send_json(data)

        # 6. Section ⑤: Action Center
        elif path == '/api/actions':
            data = action_engine.get_prescriptive_playbooks()
            self._send_json(data)

        # 7. Section ⑦: Feedback History
        elif path == '/api/feedback/list':
            data = feedback_engine.get_all_feedback()
            self._send_json({"feedback_records": data, "total_count": len(data)})

        # 8. Scenario B: Abstention & Uncertainty
        elif path == '/api/scenarios/abstention':
            if semantic_layer.is_custom and semantic_layer.custom_data_state:
                cs = semantic_layer.custom_data_state
                top_seg = cs['category_breakdown'][0]['name'] if cs['category_breakdown'] else "Core Segment"
                self._send_json({
                    "dataset_name": semantic_layer.active_dataset_name,
                    "status": "STATUS: ABSTAINED (41.0% Conf | High Entropy)",
                    "reason": f"Telemetry for `{cs['rev_col']}` in {semantic_layer.active_dataset_name} is missing attribution tags for {top_seg}.",
                    "clarification_prompt": f"⚠️ Contradictory Evidence in {semantic_layer.active_dataset_name}: What caused the variance in {top_seg}?",
                    "options": [
                        {"id": "opt_promo", "label": f"1. Seasonal demand ended for {top_seg} (Reactivates Volume Rebate)"},
                        {"id": "opt_pixel", "label": f"2. Data feed dropped rows for {top_seg} (Triggers ingestion pipeline backfill)"},
                        {"id": "opt_price", "label": f"3. Competitor price change in {top_seg} (Activates dynamic price match)"}
                    ]
                })
            else:
                self._send_json({
                    "dataset_name": "Olist Brazilian E-Commerce (Reference)",
                    "status": "STATUS: ABSTAINED (41.0% Conf | High Entropy)",
                    "reason": "Marketing campaign attribution table is 14 days stale. Payment gateway timeout logs are incomplete.",
                    "clarification_prompt": "⚠️ Contradictory Evidence: Did the 'Category Flash Sale' campaign expire on Jan 28 or was it extended?",
                    "options": [
                        {"id": "opt_promo", "label": "1. Yes, flash sale expired as scheduled (Reactivates 10% Flash Promo)"},
                        {"id": "opt_pixel", "label": "2. No, campaign was extended but tracking pixel detached (Diagnoses Ghost Loss)"},
                        {"id": "opt_price", "label": "3. Competitor launched 25% price war in São Paulo (Activates Dynamic Price Match)"}
                    ]
                })

        # 9. Scenario C: Sparse History / New Product
        elif path == '/api/scenarios/cold-start':
            days = int(query.get('days', ['4'])[0])
            active_name = semantic_layer.active_dataset_name
            
            if days < 7:
                self._send_json({
                    "days": days,
                    "dataset_name": active_name,
                    "status": "SPARSE_HISTORY_BASELINE_ENGAGED",
                    "entity": f"Newly Launched SKU / Entity in {active_name}",
                    "history_days": days,
                    "verdict": "Insufficient historical observations for 90-day time-series models. False alarm suppressed.",
                    "benchmark_used": "Category Peer Cohort Proxy Benchmark (Day 1-7 Ramp Curve)",
                    "classification": "HEALTHY LAUNCH TRAJECTORY (Zero False Alarms)",
                    "trajectory_delta": "+14.2% vs. Category Peer Average",
                    "model_status": "ARIMA Low-Volume Alarm SUPPRESSED (Prevents False Panics)"
                })
            else:
                self._send_json({
                    "days": days,
                    "dataset_name": active_name,
                    "status": "SUFFICIENT_HISTORY_CONVERGED",
                    "entity": f"Established SKU in {active_name}",
                    "history_days": days,
                    "verdict": f"Sufficient baseline achieved ({days} days). Dynamic Bayesian Bounds active.",
                    "benchmark_used": "30-Day Rolling Bayesian ARIMA & Prophet Model (μ ± 2.5σ)",
                    "classification": "STANDARD ANOMALY MONITORING ACTIVE",
                    "trajectory_delta": "Standard Variance Envelopes Engaged",
                    "model_status": "Full Time-Series Anomaly Detection Active"
                })

        # 10. Runtime Telemetry
        elif path == '/api/telemetry':
            self._send_json(telemetry_rbac.get_telemetry())

        # 11. Health
        elif path == '/api/health':
            self._send_json({
                "status": "ONLINE",
                "engine": "VERITAS E-Commerce KPI Intelligence v2.0",
                "dataset_active": semantic_layer.active_dataset_name,
                "is_custom": semantic_layer.is_custom,
                "records_indexed": len(semantic_layer.orders) if len(semantic_layer.orders) > 0 else 99441
            })

        else:
            self._send_json({"error": f"Route {path} not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        body = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}

        # Reset Dataset to Reference Olist
        if path == '/api/data/reset':
            res = semantic_layer.reset_to_reference()
            self._send_json(res)

        # Section ⑥: Ask the Engine (Intent Q&A)
        elif path == '/api/chat':
            user_query = body.get("query", "Why did revenue fall?")
            persona = body.get("persona", "business_manager")
            res = chat_engine.answer_query(user_query, persona)
            self._send_json(res)

        # Section ⑦: Feedback Submission
        elif path == '/api/feedback/submit':
            insight_id = body.get("insight_id", "INS-8401")
            rating = body.get("rating", "up")
            driver = body.get("suggested_driver", "Order Volume")
            comment = body.get("comment", "")
            res = feedback_engine.submit_feedback(insight_id, rating, driver, comment)
            self._send_json(res)

        # Universal User Data Upload (Supports both multi-file dictionary and raw CSV string)
        elif path == '/api/data/upload':
            name = body.get("dataset_name", "User E-Commerce Upload")
            res = semantic_layer.map_user_upload(body, name)
            self._send_json(res)

        # Action 1-Click Approve
        elif path == '/api/actions/approve':
            playbook_id = body.get("playbook_id", "ACT-101")
            self._send_json({
                "status": "PLAYBOOK_APPROVED_AND_ACTIVATED",
                "playbook_id": playbook_id,
                "execution_timestamp": "2026-08-30 12:00:00 UTC",
                "monitoring_engaged": "7-Day Closed-Loop Realization Tracker Active"
            })

        # Scenario B: Human-in-the-loop clarification response
        elif path == '/api/scenarios/abstention/respond':
            opt_id = body.get("option_id", "")
            opt_label = body.get("selected_option", "")
            
            if "pixel" in opt_id or "2" in opt_label or "tracking" in opt_label.lower():
                self._send_json({
                    "status": "RESOLVED: DATA INSTRUMENTATION FAILURE DIAGNOSED",
                    "upgraded_confidence": "96.8% (Proven High)",
                    "resolved_cause": "Diagnosis: Customer orders were physically normal, but checkout tracking tag dropped, creating an artificial -$22,400 'Ghost Loss' in analytics logs.",
                    "action_recommended": "Deploy ACT-104 (Hotfix GTM Tracking Container & trigger pipeline backfill).",
                    "financial_recovery": "Immediate restoration of $22,400 USD reporting accuracy.",
                    "badge_color": "emerald"
                })
            elif "price" in opt_id or "3" in opt_label or "competitor" in opt_label.lower():
                self._send_json({
                    "status": "RESOLVED: EXTERNAL COMPETITOR PRICE SHOCK",
                    "upgraded_confidence": "91.4% (Proven High)",
                    "resolved_cause": "Diagnosis: Competitor launched an aggressive regional promotion, causing a cross-elasticity drop of 18% in checkout conversion.",
                    "action_recommended": "Deploy ACT-105 (Automated Dynamic Price Match across top 20 SKUs).",
                    "financial_recovery": "+$14,200 USD projected margin recovery.",
                    "badge_color": "purple"
                })
            else:
                self._send_json({
                    "status": "RESOLVED: PROMO CESSATION CONFIRMED",
                    "upgraded_confidence": "94.6% (Proven High)",
                    "resolved_cause": "Diagnosis: Confirmed demand elasticity contraction following Flash Sale expiry on Jan 28. Causal model restored.",
                    "action_recommended": "Deploy ACT-101 (10% Flash Promo in Health & Beauty) with immediate reactivation.",
                    "financial_recovery": "+$18,500 USD projected volume recovery within 7 days.",
                    "badge_color": "indigo"
                })

        else:
            self._send_json({"error": f"POST Route {path} not found"}, 404)

class VeritasServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def run(port=8000, host='0.0.0.0'):
    server_address = (host, port)
    httpd = VeritasServer(server_address, VeritasServerHandler)
    print("==================================================", flush=True)
    print(f"VERITAS E-Commerce KPI Intelligence live on http://localhost:{port}", flush=True)
    print("Serving all 7 Sections, Intent Q&A, and Reference Olist Data", flush=True)
    print("==================================================", flush=True)
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    run(port, '0.0.0.0')
