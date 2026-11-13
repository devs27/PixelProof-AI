<div align="center">

<p align="center">
  <img src="static/img/logo.png" alt="PixelProof AI Official Logo" width="340" />
</p>

# PixelProof AI
### Autonomous Deepfake Scanner, Antivirus Quarantine & Visual Forensics Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Serverless%20Ready-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Access](https://img.shields.io/badge/Access-Public%20%2F%20Zero--Auth-00E676?style=for-the-badge&logo=shield&logoColor=black)]()
[![Model](https://img.shields.io/badge/Model-ViT--B%2F16%20%2B%20Forensic%20Engine-FF6F00?style=for-the-badge&logo=pytorch&logoColor=white)](https://huggingface.co/google/vit-base-patch16-224-in21k)

<p align="center">
  <b>PixelProof AI</b> is a next-generation cyber-defense web platform for synthetic media detection.<br>
  Instead of merely reporting a probability number, PixelProof AI treats deepfakes like digital malware: enforcing <b>active quarantine locks</b>, <b>blocking unauthorized downloads (HTTP 403)</b>, <b>generating forensic watermarks</b>, and rendering <b>$4 \times 4$ explainable spatial attention heatmaps</b>.
</p>

[✨ Live Features](#-live-features) • [🏛️ Architecture](#-system-architecture) • [🔒 Security Policy](#-active-security-policy) • [☁️ Vercel Deployment](#-deploying-to-vercel) • [💻 Local Run](#-local-development)

</div>

---

## 🌟 Live Features

* **⚡ Instant Public Access (Zero Login / Zero Friction)**
  Anyone visiting the web application directly accesses the scanner. No account registration, passwords, or barriers.
* **🧪 One-Click Test Presets**
  Built-in sample controls allow evaluators to load deepfake and authentic test images with a single click—no local file uploads needed.
* **🔍 Explainable AI ($4 \times 4$ Anomaly Heatmap)**
  Decomposes the image into a $4 \times 4$ grid (16 regional patches) to reveal exactly where generative inpainting, blending anomalies, or central facial smoothing occurred.
* **🔒 Active Antivirus Quarantine & Download Blocker**
  When an image is verified as a deepfake with $\ge 90\%$ confidence, the original high-resolution file is quarantined. Direct download links are restricted with **HTTP 403 Forbidden**.
* **🛡️ Forensic Watermark & Tamper Trace**
  Quarantined files automatically receive an irreversible degraded preview: 8px Gaussian blur, semi-transparent red alert wash, repeated $-30^\circ$ diagonal warning stamps, and a public audit banner with UTC timestamps.
* **◈ Real-Time Threat Telemetry Dashboard**
  Global counters display total images analyzed, threats neutralized, quarantine counts, and the overall network clean rate.
* **☰ Permanent Audit Ledger**
  Historic log of all scans with one-click report retrieval and forensic record management.
* **⚡ Serverless-Optimized for Vercel**
  Built with dynamic `/tmp` storage resolvers and sub-30ms edge inference, deploying in under 1 minute without hitting serverless size limits.

---

## 🏛️ System Architecture

```
                                 [ User Image Upload ]
                               (JPG / PNG / WEBP, Max 16MB)
                                           │
                                           ▼
                               ┌───────────────────────┐
                               │  Flask Routing Engine │
                               │ - UUID Sanitization   │
                               │ - Serverless Storage  │
                               └───────────┬───────────┘
                                           │
                                           ▼
                               ┌───────────────────────┐
                               │   PixelProof Engine   │
                               │ - Spatial Laplacian   │
                               │ - Chromatic Variance  │
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

| Media Classification | Confidence Score | Action Taken | HTTP Enforcement | Output Preview |
|---|---|---|---|---|
| **Authentic Image** | Any Confidence | Access Approved | `200 OK` | Original high-resolution file |
| **Suspected Deepfake** | $< 90\%$ | Flagged with threat alert | `200 OK` | Original served with warning banner |
| **Confirmed Threat** | $\ge 90\%$ | **Quarantine Lockdown** | **`403 Forbidden`** | Irreversible watermarked forensic preview only |

---

## 🔬 Spatial Heatmap Interpretation

PixelProof AI projects a $4 \times 4$ normalized anomaly distribution across the image:

```
┌───────┬───────┬───────┬───────┐
│  01%  │  07%  │  27%  │  00%  │  ■ LOW RISK   (< 25%)  : Natural texture & gradient
├───────┼───────┼───────┼───────┤
│  10%  │  33%  │  56%  │  83%  │  ■ MEDIUM RISK (25-50%): Minor boundary ambiguity
├───────┼───────┼───────┼───────┤
│  21%  │  61%  │  55%  │ 100%  │  ■ HIGH RISK  (50-75%): Inconsistent color dispersion
├───────┼───────┼───────┼───────┤
│  50%  │  73%  │  83%  │  90%  │  ■ CRITICAL   (> 75%)  : Generative synthesis artifact
└───────┴───────┴───────┴───────┘
```

---

## 📁 Repository Structure (Website Files Only)

Every file in this repository is directly utilized by the web application:

```
PixelProof-AI/
├── api/
│   └── index.py            # Vercel Serverless WSGI entrypoint
├── static/
│   ├── css/main.css        # Cyber-HUD dark UI stylesheet
│   ├── js/main.js          # Core UI handlers and flash dismissal
│   ├── js/scan.js          # Pipeline animations & drag-and-drop
│   └── samples/            # Built-in deepfake & authentic test images
├── templates/
│   ├── base.html           # Master layout with cyber-defense HUD navbar
│   ├── scan.html           # Interactive scanner & sample preset buttons
│   ├── dashboard.html      # Threat telemetry & live detection statistics
│   ├── result.html         # Threat report, 4x4 heatmap & enforcement chips
│   ├── history.html        # Public audit log table
│   └── error.html          # Custom error views (403 Forbidden, 404, 500)
├── utils/
│   ├── __init__.py
│   ├── db.py               # Resilient SQLite manager (Dynamic /tmp resolver)
│   ├── detector.py         # Multi-patch spatial frequency & forensic engine
│   └── watermark.py        # PIL forensic stamp & Gaussian blur generator
├── app.py                  # Main Flask application & routing
├── requirements.txt        # Production & Vercel serverless dependencies
├── vercel.json             # Vercel deployment configuration
├── .vercelignore           # Excludes local artifacts to ensure <1MB deploy
└── README.md               # Project documentation
```

---

## ☁️ Deploying to Vercel

The website is 100% pre-configured for Vercel Serverless:

### Method 1: Deploy with Vercel Web Dashboard (Easiest)
1. Go to **[vercel.com](https://vercel.com)** and sign in.
2. Click **Add New Project** → **Import Git Repository**.
3. Choose **`devs27/PixelProof-AI`**.
4. Keep the default settings and click **Deploy**.
5. Your live URL (e.g. `https://pixelproof-ai.vercel.app`) is active in ~30 seconds!

### Method 2: Deploy with Vercel CLI
```bash
# Inside the repository directory
npx vercel

# To deploy directly to production
npx vercel --prod
```

---

## 💻 Local Development

### 1. Clone the repository
```bash
git clone https://github.com/devs27/PixelProof-AI.git
cd PixelProof-AI
```

### 2. Create virtual environment & install requirements
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch the web application
```bash
python app.py
```
Open **`http://localhost:5000`** in your browser. You will land directly on the scanner.

---

## 📡 REST API & Web Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Renders the primary scan interface with sample presets |
| `/` | `POST` | Uploads an image, executes forensic analysis, and redirects to report |
| `/dashboard` | `GET` | Live telemetry dashboard showing threats and quarantine metrics |
| `/result/<id>` | `GET` | Detailed threat report with the $4 \times 4$ spatial heatmap |
| `/history` | `GET` | Chronological audit log of scanned images |
| `/image/<file>` | `GET` | Serves original image (returns **HTTP 403** if file is locked) |
| `/preview/<file>` | `GET` | Serves the degraded watermarked preview for quarantined threats |
| `/api/stats` | `GET` | JSON endpoint returning real-time scan and threat counts |

---

## 📜 Academic Context & License
Developed as part of the **CCE Machine Learning Research Project** at **Amrita Vishwa Vidyapeetham**.  
Licensed under the **MIT License**.
