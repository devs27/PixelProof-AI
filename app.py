import os
import uuid
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort, jsonify

from utils.db import init_db, get_db
from utils.detector import predict_image
from utils.watermark import apply_watermark

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)
app.secret_key = os.environ.get("SECRET_KEY", "pixelproof-ai-public-key-2026")

# Resilient storage path resolution for local dev & Vercel serverless
def _resolve_storage():
    is_serverless = os.environ.get("VERCEL") or not os.access(BASE_DIR, os.W_OK)
    if is_serverless:
        tmp = tempfile.gettempdir()
        up = os.path.join(tmp, "pixelproof_uploads")
        pv = os.path.join(tmp, "pixelproof_previews")
    else:
        up = os.path.join(BASE_DIR, "static", "uploads")
        pv = os.path.join(BASE_DIR, "static", "previews")
    try:
        os.makedirs(up, exist_ok=True)
        os.makedirs(pv, exist_ok=True)
    except OSError:
        tmp = tempfile.gettempdir()
        up = os.path.join(tmp, "pixelproof_uploads")
        pv = os.path.join(tmp, "pixelproof_previews")
        os.makedirs(up, exist_ok=True)
        os.makedirs(pv, exist_ok=True)
    return up, pv

UPLOAD_FOLDER, PREVIEW_FOLDER = _resolve_storage()
ALLOWED_EXT    = {"jpg", "jpeg", "png", "webp"}
CONF_THRESHOLD = 0.90
app.config["UPLOAD_FOLDER"]      = UPLOAD_FOLDER
app.config["PREVIEW_FOLDER"]     = PREVIEW_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# Fallback route for static files to guarantee 100% availability on serverless
@app.route("/static/<path:filename>")
def serve_static(filename):
    target = os.path.join(STATIC_DIR, filename)
    if os.path.exists(target):
        return send_file(target)
    abort(404)

# Primary route: Direct scanner (No login required)
@app.route("/", methods=["GET", "POST"])
def scan():
    if request.method == "GET":
        return render_template("scan.html")
        
    if "image" not in request.files:
        flash("No file uploaded. Please select an image.", "danger")
        return redirect(url_for("scan"))
        
    file = request.files["image"]
    if file.filename == "":
        flash("No file selected.", "danger")
        return redirect(url_for("scan"))
        
    if not allowed_file(file.filename):
        flash("Invalid file type. Allowed formats: JPG, PNG, WEBP.", "danger")
        return redirect(url_for("scan"))
    
    ext         = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    save_path   = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file.save(save_path)
    
    label, confidence, patch_scores = predict_image(save_path, original_filename=file.filename)
    locked       = (label == "Fake") and (confidence >= CONF_THRESHOLD)
    preview_name = None
    
    if locked:
        preview_name = f"preview_{unique_name}"
        preview_path = os.path.join(app.config["PREVIEW_FOLDER"], preview_name)
        apply_watermark(save_path, preview_path, "PUBLIC_AUDITOR", confidence)
        
    db = get_db()
    db.execute("""INSERT INTO scans (user_id, filename, preview_filename, label, confidence, patch_scores, locked, scanned_at)
                  VALUES (?,?,?,?,?,?,?,?)""",
               (1, unique_name, preview_name, label, round(confidence, 4),
                str(patch_scores), 1 if locked else 0, datetime.utcnow().isoformat()))
    db.commit()
    scan_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    return redirect(url_for("result", scan_id=scan_id))

@app.route("/dashboard")
def dashboard():
    db    = get_db()
    scans = db.execute("SELECT * FROM scans ORDER BY scanned_at DESC LIMIT 20").fetchall()
    stats = db.execute("""SELECT COUNT(*) as total, 
                                 SUM(CASE WHEN label='Fake' THEN 1 ELSE 0 END) as threats,
                                 SUM(CASE WHEN locked=1 THEN 1 ELSE 0 END) as quarantined 
                          FROM scans""").fetchone()
    return render_template("dashboard.html", scans=scans, stats=stats)

@app.route("/result/<int:scan_id>")
def result(scan_id):
    db   = get_db()
    scan = db.execute("SELECT * FROM scans WHERE id=?", (scan_id,)).fetchone()
    if not scan: 
        abort(404)
    patch_scores = []
    try: 
        patch_scores = eval(scan["patch_scores"])
    except Exception: 
        pass
    return render_template("result.html", scan=scan, patch_scores=patch_scores)

@app.route("/image/<filename>")
def serve_image(filename):
    db   = get_db()
    scan = db.execute("SELECT locked FROM scans WHERE filename=?", (filename,)).fetchone()
    if not scan or scan["locked"]: 
        abort(403)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(path): 
        abort(404)
    resp = send_file(path)
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/preview/<filename>")
def serve_preview(filename):
    path = os.path.join(app.config["PREVIEW_FOLDER"], filename)
    if not os.path.exists(path): 
        abort(404)
    resp = send_file(path)
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/history")
def history():
    db    = get_db()
    scans = db.execute("SELECT * FROM scans ORDER BY scanned_at DESC LIMIT 50").fetchall()
    return render_template("history.html", scans=scans)

@app.route("/delete/<int:scan_id>", methods=["POST"])
def delete_scan(scan_id):
    db   = get_db()
    scan = db.execute("SELECT * FROM scans WHERE id=?", (scan_id,)).fetchone()
    if scan:
        for fname, folder in [(scan["filename"], app.config["UPLOAD_FOLDER"]), 
                              (scan["preview_filename"], app.config["PREVIEW_FOLDER"])]:
            if fname:
                fp = os.path.join(folder, fname)
                if os.path.exists(fp): 
                    try: os.remove(fp)
                    except OSError: pass
        db.execute("DELETE FROM scans WHERE id=?", (scan_id,))
        db.commit()
        flash("Scan record deleted.", "success")
    return redirect(url_for("history"))

@app.route("/api/stats")
def api_stats():
    db    = get_db()
    stats = db.execute("""SELECT COUNT(*) as total, 
                                 SUM(CASE WHEN label='Fake' THEN 1 ELSE 0 END) as threats,
                                 SUM(CASE WHEN locked=1 THEN 1 ELSE 0 END) as quarantined,
                                 ROUND(AVG(confidence)*100,2) as avg_confidence 
                          FROM scans""").fetchone()
    return jsonify(dict(stats))

@app.route("/favicon.ico")
def favicon():
    fav_path = os.path.join(app.root_path, "static", "img", "favicon.ico")
    if os.path.exists(fav_path):
        return send_file(fav_path, mimetype="image/vnd.microsoft.icon")
    abort(404)

@app.errorhandler(403)
def forbidden(e): 
    return render_template("error.html", code=403, msg="Access denied. Image is locked by security policy."), 403

@app.errorhandler(404)
def not_found(e): 
    return render_template("error.html", code=404, msg="Resource not found."), 404

@app.errorhandler(413)
def too_large(e): 
    return render_template("error.html", code=413, msg="File too large. Maximum size is 16 MB."), 413

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, msg="Internal server error. Please try again."), 500

with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"[PixelProof AI] DB init notice: {e}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
