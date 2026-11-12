<div align="center">

# 🛡️ PixelProof AI
### AI-Powered Deepfake Detection, Antivirus Quarantine & Visual Forensics Framework

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![ViT](https://img.shields.io/badge/Model-Vision%20Transformer%20(ViT--B%2F16)-orange.svg)](https://huggingface.co/google/vit-base-patch16-224-in21k)
[![Vercel](https://img.shields.io/badge/Deployment-Vercel%20Serverless-black.svg)](https://vercel.com)
[![Access](https://img.shields.io/badge/Access-Public%20%2F%20Zero--Login-brightgreen.svg)]()

<p align="center">
  <b>PixelProof AI</b> treats manipulated media like digital malware. Rather than simply displaying a percentage probability, it enforces an active cybersecurity threat policy: real-time spatial patch explainability, automated quarantine lockdown, direct download prevention (HTTP 403), and irreversible forensic watermarking.
</p>

[Quick Start](#-quick-start-local) • [Vercel Deployment](#-deploy-to-vercel) • [Architecture](#-architecture--workflow) • [Security Policy](#-active-security-policy)

</div>

---

## 🌟 Key Capabilities

* **Instant Public Access (Zero-Login / No Friction)**:
  Anyone visiting the web application lands directly on the scanner. No accounts, passwords, or authentication barriers required.
* **Dual-Tier Detection Engine**:
  * **Tier 1 (ViT-B/16 Vision Transformer)**: Deep self-attention extraction across 12 transformer layers when running locally or on GPU servers.
  * **Tier 2 (PixelProof Native Forensic Engine)**: High-frequency Laplacian spatial gradient and multi-patch chromatic dispersion analysis designed for instant execution on Vercel Serverless (<30ms response, zero cold-start delay).
* **Explainable AI ($4 \times 4$ Anomaly Heatmap)**:
  Extracts patch anomaly scores across 16 image regions, pinpointing unnatural blending, synthetic central facial smoothing, or generative artifact clusters.
* **Active Threat Quarantine**:
  When a synthetic image exceeds the confidence threshold ($\ge 90\%$), direct download is **quarantined and blocked with HTTP 403 Forbidden**.
* **Forensic Watermarking & Public Audit Stamp**:
  Generates an irreversible preview degraded with an 8px Gaussian blur, red wash overlay, $-30^\circ$ diagonal security stamps, and UTC timestamp audit banners.
* **Threat Telemetry Dashboard & Audit Log**:
  Tracks global scan counts, threat detection ratios, quarantine numbers, and scan history.
* **One-Click Pre-loaded Samples**:
  Includes built-in deepfake and authentic sample presets for one-click testing without uploading personal files.

---

## 🏛️ Architecture & Workflow

```
                                 [ User Image Upload ]
                               (JPG / PNG / WEBP, Max 16MB)
                                           │
                                           ▼
                               ┌───────────────────────┐
                               │    Flask Web Engine   │
                               │ - UUID Sanitization   │
                               │ - Resilient Storage   │
                               └───────────┬───────────┘
                                           │
                                           ▼
                               ┌───────────────────────┐
                               │    Inference Engine   │
                               │ - ViT-B/16 / Forensic │
                               │ - 4x4 Patch Analysis  │
                               └───────────┬───────────┘
                                           │
                     ┌─────────────────────┴─────────────────────┐
                     ▼                                           ▼
            [ AUTHENTIC IMAGE ]                         [ DEEPFAKE DETECTED ]
              Confidence: Any                             Confidence Check:
             Original Approved                           ┌─────────┴─────────┐
             HTTP 200 Served                             ▼                   ▼
                                                    [ < 90% Conf ]      [ ≥ 90% Conf ]
                                                    Flagged threat     🔒 QUARANTINE LOCK
                                                    Original served            │
                                                                               ▼
                                                                     ┌───────────────────┐
                                                                     │ Watermark Engine  │
                                                                     │ - 8px Blur + Wash │
                                                                     │ - Diagonal Stamps │
                                                                     │ - HTTP 403 on orig│
                                                                     └───────────────────┘
```

---

## 🔒 Active Security Policy

| Condition | Verdict | System Action | Enforcement Level |
|---|---|---|---|
| **Authentic Image** | Real (Any %) | Direct access approved | `HTTP 200 OK` (Original image served) |
| **Suspected Manipulation** | Fake (< 90%) | Flagged as threat | `HTTP 200 OK` (Warning badge displayed) |
| **Confirmed Deepfake** | Fake ($\ge$ 90%) | **Quarantine Lockdown** | **`HTTP 403 Forbidden`** on original · Watermarked audit preview only |

---

## 📁 Repository Structure

```
PixelProof-AI/
├── api/
│   └── index.py            # Vercel Serverless WSGI entrypoint
├── models/
│   ├── README.md           # Model weight setup instructions
│   └── my_deepfake_model/  # Model configurations & processor configs
├── static/
│   ├── css/main.css        # Cyber-HUD dark UI styling
│   ├── js/main.js          # Core UI handlers
│   ├── js/scan.js          # Pipeline animations & drag-and-drop
│   └── samples/            # Pre-loaded deepfake and authentic test images
├── templates/
│   ├── base.html           # Master layout with cyber-defense HUD navbar
│   ├── scan.html           # Interactive radar scanner & sample loader
│   ├── dashboard.html      # Threat telemetry & detection statistics
│   ├── result.html         # Threat report, 4x4 heatmap & enforcement chips
│   ├── history.html        # Public audit log table
│   └── error.html          # Custom error views (403, 404, 413, 500)
├── utils/
│   ├── __init__.py
│   ├── db.py               # Resilient SQLite manager (Dynamic /tmp resolver)
│   ├── detector.py         # Dual-tier Vision Transformer & Forensic engine
│   └── watermark.py        # PIL forensic stamp & blur generator
├── app.py                  # Main Flask application
├── requirements.txt        # Production & Vercel serverless dependencies
├── requirements-local.txt  # Full dependencies including local PyTorch/ViT
├── vercel.json             # Vercel deployment configuration
├── .vercelignore           # Prevents uploading heavy files to serverless
└── README.md
```

---

## 🚀 Quick Start (Local)

### 1. Clone the repository
```bash
git clone https://github.com/devs27/PixelProof-AI.git
cd PixelProof-AI
```

### 2. Create virtual environment & install dependencies
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

*(Optional: To run full local PyTorch ViT inference, install `pip install -r requirements-local.txt`)*

### 3. Run the application
```bash
python app.py
```
Open **`http://localhost:5000`** in your browser. You will land directly on the scanner.

---

## ☁️ Deploy to Vercel

### Method 1: Deploy with Vercel CLI (Recommended)
```bash
# Inside project directory
npx vercel

# Deploy directly to production
npx vercel --prod
```

### Method 2: Deploy via Vercel Web Dashboard
1. Fork or push this repository to your GitHub account: `https://github.com/devs27/PixelProof-AI`.
2. Go to [Vercel Dashboard](https://vercel.com) and click **Add New Project**.
3. Import **`PixelProof-AI`**.
4. Leave settings as default (Framework: Other, Root directory: `./`).
5. Click **Deploy**. Vercel will build and host your app on a live `https://<your-project>.vercel.app` URL within seconds!

---

## 🔬 Explainable AI: $4 \times 4$ Attention Heatmap

PixelProof AI decomposes the input image into 16 spatial patches. High-frequency anomaly scores are calculated for each patch, visualizing where generative artifacts or unnatural blending occurred:

```
┌───────┬───────┬───────┬───────┐
│  01%  │  07%  │  27%  │  00%  │  Low Risk  (< 25%)  : Safe / Natural
├───────┼───────┼───────┼───────┤
│  10%  │  33%  │  56%  │  83%  │  Med Risk  (25-50%): Boundary Ambiguity
├───────┼───────┼───────┼───────┤
│  21%  │  61%  │  55%  │ 100%  │  High Risk (50-75%): Feature Inconsistency
├───────┼───────┼───────┼───────┤
│  50%  │  73%  │  83%  │  90%  │  Critical  (> 75%)  : Generative Artifacts
└───────┴───────┴───────┴───────┘
```

---

## 📜 License & Acknowledgments
Developed as part of the CCE Machine Learning Research Project at Amrita Vishwa Vidyapeetham.
Designed for forensic auditing, educational research, and endpoint synthetic media protection.
