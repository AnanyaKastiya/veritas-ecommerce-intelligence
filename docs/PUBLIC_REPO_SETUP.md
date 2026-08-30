# VERITAS: Public Repository & Submission Setup Guide
> **Accenture Innovation Challenge 2026 — Prototype Submission Guide**  
> *Deadline: 30th August, 2026, 11:59 PM*

---

## 1. Step-by-Step GitHub Repository Setup

To submit your working prototype to Accenture, initialize a Git repository and push it to a public GitHub repository:

```bash
# 1. Open terminal inside the project directory:
cd C:\Users\anany\.gemini\antigravity\scratch\veritas-bi

# 2. Initialize Git and add all files
git init
git add .
git commit -m "feat: VERITAS Autonomous KPI Intelligence-to-Action Engine Prototype v2.0"

# 3. Create a new public repository on GitHub named 'veritas-kpi-engine'
# 4. Link your remote repository and push
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/veritas-kpi-engine.git
git branch -M main
git push -u origin main
```

---

## 2. Generating the Required PDF Submission Document (< 20 MB)

The competition requires a **README Document (Format - PDF, max 20 MB)** covering solution approach, architecture, implementation, key features, and evaluation.

### Recommended Method 1: VS Code Markdown PDF Export
1. Install the **Markdown PDF** extension in VS Code.
2. Open `docs/README.md`.
3. Right-click anywhere in the file and select **Markdown PDF: Export (pdf)**.
4. Save the generated `README.pdf` file.

### Recommended Method 2: Python / Pandoc CLI
```bash
# Convert Markdown to clean PDF using python-markdown or pandoc:
pandoc docs/README.md -o docs/VERITAS_Submission_Documentation.pdf --pdf-engine=wkhtmltopdf
```

### Recommended Method 3: Browser Print to PDF
1. Open `docs/README.md` in any GitHub / Markdown previewer or browser.
2. Press `Ctrl + P` (Print), select **Save as PDF**, set Margins to *Default*, and check *Background Graphics*.

---

## 3. Recording Your 3-Minute Video Pitch

Follow the exact script and storyboard in `docs/DEMO_SCRIPT_STORYBOARD.md`:
1. **Tool Recommendations**: Loom, OBS Studio, or Zoom (Local Recording).
2. **Setup**:
   - Run `python backend/server.py` and open `http://localhost:8000/` in full-screen (1080p).
   - Set webcam in picture-in-picture in the top-right corner.
3. **Pacing**:
   - 0:00 – 0:25: Problem & High-Level Architecture (Presenter 1)
   - 0:25 – 1:25: Live KPI Ribbon & AI Courtroom Debate (Presenter 2)
   - 1:25 – 1:50: Persona Toggle & Live RBAC Masking (Presenter 1)
   - 1:50 – 2:40: Slack Poll Abstention & Option 3B Action Efficacy Tracker (Presenter 2)
   - 2:40 – 3:00: Telemetry Economics & Business ROI Closing (Presenter 1)
4. **Hosting**: Upload to **YouTube (Unlisted or Public)** or **Google Drive (Set permission to "Anyone with the link can view")**.

---

## 4. Final Submission Checklist

- [x] **Working Prototype**: Verified locally on `http://localhost:8000/`.
- [x] **Deterministic Math & Semantic Contract**: `config/kpi_contract.yaml` and `engine/driver_decomposition.py`.
- [x] **Adversarial AI Courtroom**: `engine/causal_tribunal.py` with 3 agents and SCM verdict.
- [x] **Persona-Specific RBAC**: `engine/rbac_security.py` and `engine/narrative_generator.py`.
- [x] **Edge Case 1 (Abstention & Slack Poll)**: `engine/abstention_engine.py`.
- [x] **Edge Case 2 (Cold-Start Austin Hub)**: `engine/sparse_history_engine.py`.
- [x] **Edge Case 3 (Option 3B Action Efficacy Tracker)**: `engine/action_efficacy_tracker.py`.
- [x] **Telemetry & Economics**: `engine/telemetry.py` (<$0.0002/insight, 784ms latency).
- [x] **README.md & PDF Documentation**: `docs/README.md`.
- [x] **Enterprise Business Proposal**: `docs/BUSINESS_PROPOSAL.md`.
- [x] **3-Minute Video Script**: `docs/DEMO_SCRIPT_STORYBOARD.md`.
- [x] **GitHub Public Repository URL**: Ready for push.
