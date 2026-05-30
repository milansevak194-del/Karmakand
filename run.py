import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ==============================
# 🔹 DATABASE CONFIGURATION (HYBRID FOR LOCAL & ONLINE)
# ==============================
# If online database variables exist, it will use them; otherwise, defaults to local XAMPP
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'karmakand')
# Aiven or online DBs usually use port 3306 or specified ports. Local is 3306.
DB_PORT = os.environ.get('DB_PORT', '3306')

try: 
    db = mysql.connector.connect(  
        host=DB_HOST,      
        user=DB_USER,           
        password=DB_PASSWORD,           
        database=DB_NAME,
        port=int(DB_PORT)
    )
    cursor = db.cursor(dictionary=True)
    print("✅ DB Connected Successfully!")

    # ==============================
    # 🔹 CREATE TABLES IF NOT EXISTS
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
    print("✅ Tables Checked and Created Successfully!")

except mysql.connector.Error as e:
    print("❌ DB Connection Error:", e)
    print("💡 Tip: If running locally, check if MySQL is 'Started' in XAMPP Control Panel.")
    db = None
    cursor = None


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
    if not db or not cursor:
        return "❌ Database connection is not active!", 500
        
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    pooja = request.form.get("pooja")
    date = request.form.get("date")

    try:
        query = "INSERT INTO bookings (name, mobile, pooja, date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, mobile, pooja, date))
        db.commit()
        return "✅ Booking Saved Successfully"
    except Exception as e:
        return f"❌ Error saving booking to database: {e}", 500


# VIEW BOOKINGS (TEST)
@app.route("/data")
def data():
    if not cursor:
        return "❌ Database connection is not active!", 500
        
    cursor.execute("SELECT * FROM bookings")
    data_results = cursor.fetchall()
    return jsonify(data_results)


# ==============================
# 🔹 RUN SERVER (DYNAMIC FOR RENDER hosting)
# ==============================
if __name__ == "__main__":
    # Render cloud hosting provides a dynamic port via environment variable. 
    # If not found (like running locally), it will default to 5000.
    server_port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=server_port, debug=True)