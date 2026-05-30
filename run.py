from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import mysql.connector

app = Flask(__name__)

# ==============================
# 🔹 DATABASE CONNECTION 
# ==============================
try: 
    db = mysql.connector.connect(  
        host='127.0.0.1',      
        user='root',           
        password='',           
        database='karmakand'   
    )
    cursor = db.cursor(dictionary=True)
    print("✅ DB Connected Successfully!")

    # ==============================
    # 🔹 CREATE TABLES 
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
    print("✅ Tables Checked/Created!")

except mysql.connector.Error as e:
    print("❌ DB Connection Error:", e)
    print("💡 ટિપ: ચેક કરો કે XAMPP માં MySQL 'Start' છે કે નહીં?")
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
        return "❌ Database not connected!", 500
        
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    pooja = request.form.get("pooja")
    date = request.form.get("date")

    try:
        query = "INSERT INTO bookings (name, mobile, pooja, date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, mobile, pooja, date))
        db.commit()
        return "✅ Booking Saved"
    except Exception as e:
        return f"❌ Error saving booking: {e}", 500


# VIEW BOOKINGS (TEST)
@app.route("/data")
def data():
    if not cursor:
        return "❌ Database not connected!", 500
        
    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()
    return jsonify(data)


# ==============================
# 🔹 RUN
# ==============================
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)