import os
import yaml
import json
from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from engine.anomaly_detector import AnomalyDetector
from engine.driver_decomposition import DriverDecompositionEngine
from engine.causal_tribunal import CausalTribunal
from engine.abstention_engine import AbstentionEngine
from engine.sparse_history_engine import SparseHistoryEngine
from engine.action_efficacy_tracker import ActionEfficacyTracker
from engine.narrative_generator import NarrativeGenerator
from engine.rbac_security import RBACSecurityEngine
from engine.telemetry import RuntimeTelemetry

app = FastAPI(
    title="VERITAS: Autonomous KPI Intelligence-to-Action Engine",
    version="2.0.0",
    description="Round 2 Working Prototype for Accenture Innovation Challenge 2026"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

anomaly_engine = AnomalyDetector()
driver_engine = DriverDecompositionEngine()
tribunal_engine = CausalTribunal()
abstention_engine = AbstentionEngine()
sparse_engine = SparseHistoryEngine()
efficacy_engine = ActionEfficacyTracker()
narrative_engine = NarrativeGenerator()
rbac_engine = RBACSecurityEngine()
telemetry_engine = RuntimeTelemetry()

@app.get("/api/health")
def health_check():
    return {"status": "ONLINE", "engine": "VERITAS v2.0", "timestamp": "2026-08-28T00:00:00Z"}

@app.get("/api/contract")
def get_kpi_contract():
    with open("config/kpi_contract.yaml", "r", encoding="utf-8") as f:
        contract = yaml.safe_load(f)
    return contract

@app.get("/api/kpis")
def get_live_kpis(persona: str = Query("executive_vp")):
    anom = anomaly_engine.analyze_latest_window()
    raw_payload = {
        "region": "Southwest_Dallas_Hub",
        "kpis": [
            {
                "id": "gmv",
                "name": "Gross Merchandise Value (GMV)",
                "current_value": "$303,165.15",
                "expected_value": "$375,400.00",
                "delta_pct": "-19.24%",
                "status": "CRITICAL_ANOMALY",
                "unit": "USD",
                "sparkline": [42000, 48000, 52000, 49000, 51000, 38000, 31000, 24000]
            },
            {
                "id": "order_volume",
                "name": "Completed Order Volume",
                "current_value": "8,612 orders",
                "expected_value": "10,200 orders",
                "delta_pct": "-15.57%",
                "status": "WARNING",
                "unit": "orders",
                "sparkline": [1200, 1350, 1420, 1380, 1400, 1100, 950, 812]
            },
            {
                "id": "aov",
                "name": "Average Order Value (AOV)",
                "current_value": "$35.20",
                "expected_value": "$34.50",
                "delta_pct": "+2.03%",
                "status": "HEALTHY",
                "unit": "USD",
                "sparkline": [34.2, 34.5, 34.6, 34.4, 34.5, 35.1, 35.2, 35.2]
            },
            {
                "id": "delivery_sla_breach",
                "name": "Delivery SLA Breach Rate",
                "current_value": "28.40%",
                "expected_value": "4.80%",
                "delta_pct": "+491.6%",
                "status": "SEVERE_BREACH",
                "unit": "percentage",
                "sparkline": [4.2, 4.5, 5.1, 4.8, 6.2, 14.5, 22.1, 28.4]
            },
            {
                "id": "customer_refund_rate",
                "name": "Support Escalation & Refund Rate",
                "current_value": "14.20%",
                "expected_value": "3.20%",
                "delta_pct": "+343.8%",
                "status": "HIGH_ALERT",
                "unit": "percentage",
                "sparkline": [3.1, 3.2, 3.0, 3.3, 3.5, 7.8, 11.2, 14.2]
            }
        ],
        "gross_margin_usd": "$86,402.00 USD (Margin: 28.5%)",
        "executive_bonus_pool": "$12,500.00 USD",
        "active_persona": persona
    }
    
    return rbac_engine.apply_security_masking(persona, raw_payload)

@app.post("/api/analyze")
def run_complete_analysis(persona: str = Query("executive_vp")):
    telemetry_engine.start_timer()

    anomaly_result = anomaly_engine.analyze_latest_window()
    driver_result = driver_engine.calculate_pvm_decomposition()
    tribunal_result = tribunal_engine.run_tribunal_debate(anomaly_result, driver_result)
    narrative_result = narrative_engine.generate_persona_narrative(
        persona, anomaly_result, driver_result, tribunal_result
    )
    telemetry_result = telemetry_engine.get_runtime_metrics(prompt_tokens=320, completion_tokens=195)

    response_data = {
        "anomaly_detection": anomaly_result,
        "pvm_decomposition": driver_result,
        "tribunal_courtroom": tribunal_result,
        "persona_narrative": narrative_result,
        "telemetry": telemetry_result,
        "active_persona": persona
    }

    return rbac_engine.apply_security_masking(persona, response_data)

@app.get("/api/scenarios/abstention")
def get_abstention_scenario():
    return abstention_engine.evaluate_contradiction_scenario()

@app.post("/api/scenarios/abstention/respond")
def respond_slack_poll(payload: dict = Body(...)):
    option_text = payload.get("selected_option_text", "Yes, tracking pixel detached")
    return abstention_engine.submit_slack_poll_response(option_text)

@app.get("/api/scenarios/cold-start")
def get_cold_start_scenario():
    return sparse_engine.analyze_cold_start()

@app.get("/api/actions/efficacy")
def get_action_efficacy_board():
    return efficacy_engine.get_efficacy_history()

@app.post("/api/actions/approve")
def approve_prescriptive_action(payload: dict = Body(...)):
    playbook_name = payload.get("playbook_name", "Emergency 3PL Fleet Failover + $10 Customer Rebates")
    driver = payload.get("driver", "Dallas Hub Capacity Bottleneck")
    approved_by = payload.get("approved_by", "Executive VP Commercial")
    cost_usd = payload.get("cost_usd", 15000.0)
    projected_recovery_usd = payload.get("projected_recovery_usd", 42000.0)

    record = efficacy_engine.execute_and_log_action(
        playbook_name, driver, approved_by, cost_usd, projected_recovery_usd
    )
    return {"status": "ACTION_APPROVED_AND_LOGGED", "record": record}

@app.get("/api/telemetry")
def get_telemetry_metrics():
    return telemetry_engine.get_runtime_metrics()

if os.path.exists("frontend/index.html"):
    @app.get("/")
    def serve_frontend():
        return FileResponse("frontend/index.html")

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(open("backend/main.py", "r", encoding="utf-8").read() if os.path.exists("backend/main.py") else "")
