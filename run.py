from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import mysql.connector

app = Flask(__name__)

# ==============================
# 🔹 DATABASE CONNECTION
# ==============================
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


# ==============================
# 🔹 CREATE TABLES (AUTO)
# ==============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    mobile VARCHAR(20),
    pooja VARCHAR(100),
    date VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS brahmins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    mobile VARCHAR(20)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS yajmans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    mobile VARCHAR(20)
)
""")

db.commit()


# ==============================
# 🔹 ROUTES
# ==============================

# HOME
@app.route("/")
def home():
    return render_template("home.html")


# BOOKING PAGE
@app.route("/yajman")
def yajman():
    return render_template("yajman_booking.html")


# SAVE BOOKING
@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    pooja = request.form.get("pooja")
    date = request.form.get("date")

    query = "INSERT INTO bookings (name, mobile, pooja, date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, mobile, pooja, date))
    db.commit()

    return "✅ Booking Saved"


# VIEW BOOKINGS (TEST)
@app.route("/data")
def data():
    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()
    return jsonify(data)


# ==============================
# 🔹 RUN
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)s