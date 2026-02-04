# app.py  -- Unified Flask app: Auth + AI endpoints
import os
import sqlite3
import sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# --- load env ---
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Config
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "please_change_this_secret")
FRONTEND_APP_TOKEN = os.environ.get("FRONTEND_APP_TOKEN", "123456")
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "database.db"))

# --- try import ai_proxy (if missing provide stub) ---
ai_proxy_available = True
_ai_import_error = None
try:
    # attempt to import your ai_proxy module (should be in same folder or adjust PYTHONPATH)
    from ai_proxy import generate_content, list_models
except Exception as exc:
    ai_proxy_available = False
    _ai_import_error = str(exc)
    def generate_content(request_body, model=None):
        return {"error": "ai_proxy not available", "detail": _ai_import_error}
    def list_models():
        return {"error": "ai_proxy not available", "detail": _ai_import_error}

# --- Flask app ---
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = SECRET_KEY

# --- Database helpers ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Password verification that supports legacy plaintext passwords:
def verify_password(stored_password, provided_password):
    """
    If stored_password looks like a werkzeug hash (starts with method name), use check_password_hash.
    Otherwise treat stored_password as legacy plaintext: compare directly and return True and a rehash flag.
    """
    if stored_password.startswith("pbkdf2:") or stored_password.startswith("argon2:") or stored_password.startswith("scrypt:"):
        return check_password_hash(stored_password, provided_password), False
    # legacy plaintext
    return (stored_password == provided_password), True

def create_user(username, password):
    hashed = generate_password_hash(password)
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, "username_exists"
    finally:
        conn.close()

def get_user(username):
    conn = get_db_connection()
    c = conn.cursor()
    row = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row

def upgrade_password_hash_if_needed(username, new_hashed):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed, username))
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# --- Routes: Auth + Pages ---
@app.route("/")
def root():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Vui lòng điền tài khoản và mật khẩu.", "error")
            return redirect(url_for("login"))

        if action == "register":
            ok, err = create_user(username, password)
            if ok:
                flash("Đăng ký thành công! Hãy đăng nhập.", "success")
            else:
                if err == "username_exists":
                    flash("Tên tài khoản đã tồn tại!", "error")
                else:
                    flash("Lỗi khi tạo tài khoản.", "error")
            return redirect(url_for("login"))

        elif action == "login":
            user = get_user(username)
            if user:
                stored_pw = user["password"]
                verified, legacy_plain = verify_password(stored_pw, password)
                if verified:
                    # if legacy plaintext, upgrade the stored hash
                    if legacy_plain:
                        new_hash = generate_password_hash(password)
                        upgrade_password_hash_if_needed(username, new_hash)
                    session["username"] = username
                    return redirect(url_for("dashboard"))
            flash("Sai tài khoản hoặc mật khẩu!", "error")
    # GET
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    # Provide FRONTEND_APP_TOKEN to client for AI JS calls (this token is only for app-level auth)
    return render_template("dashboard.html", username=session["username"], app_token=FRONTEND_APP_TOKEN)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# --- API endpoints for AI (require X-APP-TOKEN header) ---
@app.route("/api/list-models", methods=["GET"])
def api_list_models():
    token = request.headers.get("X-APP-TOKEN")
    if token != FRONTEND_APP_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    res = list_models()
    return jsonify(res)

@app.route("/api/generate", methods=["POST"])
def api_generate():
    token = request.headers.get("X-APP-TOKEN")
    if token != FRONTEND_APP_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    model = body.get("model")
    request_body = body.get("requestBody")
    if request_body is None:
        return jsonify({"error": "Missing requestBody"}), 400

    try:
        res = generate_content(request_body=request_body, model=model)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal error calling AI", "detail": str(exc)}), 500

    if isinstance(res, dict) and res.get("error"):
        return jsonify({"error": "AI call failed", "detail": res}), 502

    return jsonify(res)

# --- simple health check route ---
@app.route("/health")
def health():
    return jsonify({"status": "ok", "ai_proxy_available": ai_proxy_available})

# --- Run ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting app on 0.0.0.0:{port}  (AI proxy available: {ai_proxy_available})")
    app.run(host="0.0.0.0", port=port, debug=True)
