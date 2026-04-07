from flask import Flask, render_template, request, jsonify, redirect, url_for
from Karma import KarmaAI
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ai = KarmaAI()

# ==============================
# 🏠 HOME
# ==============================
@app.route("/")
def home():
    return render_template("home.html")

# ==============================
# 🧘 BRAHMIN LOGIN
# ==============================
@app.route("/brahmin")
def brahmin():
    return render_template("brahmin_login.html")

# ==============================
# 🔥 BRAHMIN VERIFY
# ==============================
@app.route("/brahmin_verify", methods=["POST"])
def brahmin_verify():

    name = request.form.get("name")
    mobile = request.form.get("mobile")

    # FILES
    marksheet10 = request.files.get("marksheet10")

    def save_file(file):
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            return filename
        return ""

    save_file(marksheet10)

    # AI VERIFY
    result = ai.process(name + " " + mobile)

    if result:
        return redirect(url_for("brahmin"))

    return render_template("brahmin_login.html", result="Verification Failed ❌")


# ==============================
# 📿 YAJMAN PAGE
# ==============================
@app.route("/yajman")
def yajman():
    return render_template("yajman_booking.html")


# ==============================
# 💰 PAYMENT PAGE
# ==============================
@app.route("/payment")
def payment():
    return render_template("payment.html")


# ==============================
# 🚀 RUN (FOR RENDER)
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)