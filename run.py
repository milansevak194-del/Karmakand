from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from Karma import KarmaAI
import os
import mysql.connector

app = Flask(__name__)

# =========================
# 🔥 DATABASE CONNECTION
# =========================
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = db.cursor(dictionary=True)
    print("✅ DB Connected")
except Exception as e:
    print("❌ DB Error:", e)

# =========================
# 📁 UPLOAD FOLDER
# =========================
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# 🤖 AI INIT
# =========================
ai = KarmaAI()

# =========================
# 🏠 HOME
# =========================
@app.route("/")
def home():
    return render_template("home.html")

# =========================
# 👨‍🦳 BRAHMIN LOGIN
# =========================
@app.route("/brahmin")
def brahmin():
    return render_template("brahmin_login.html")

# =========================
# 🔐 VERIFY
# =========================
@app.route("/brahmin_verify", methods=["POST"])
def brahmin_verify():
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    file = request.files.get("marksheet10")

    filename = ""
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

    # AI check
    result = ai.process(name + " " + mobile)

    if result:
        return redirect(url_for("brahmin"))

    return render_template("brahmin_login.html", result="Verification Failed ❌")

# =========================
# 🧍 YAJMAN PAGE
# =========================
@app.route("/yajman")
def yajman():
    return render_template("yajman_booking.html")

# =========================
# 💰 PAYMENT PAGE
# =========================
@app.route("/payment")
def payment():
    return render_template("payment.html")

# =========================
# 🚀 RUN (FOR RAILWAY)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)