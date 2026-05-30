import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ==========================================
# 🔹 DATABASE CONFIGURATION
# ==========================================
# Fetching database credentials from environment variables for production security.
# Defaults to local XAMPP/MySQL environment configuration if not found.
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'karmakand')
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
    print("✅ Database Connected Successfully!")

    # 🔹 Creating the 'brahmins' table with all required fields if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS brahmins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        mobile VARCHAR(20),
        pathshala VARCHAR(200),
        veda VARCHAR(100),
        shakha VARCHAR(100),
        marksheet10 VARCHAR(255),
        marksheet12 VARCHAR(255),
        certificate VARCHAR(255),
        aadhar VARCHAR(255),
        pan VARCHAR(255),
        photo VARCHAR(255)
    )
    """)
    db.commit()
    print("✅ Database Tables Verified and Synchronized Successfully!")

except mysql.connector.Error as e:
    print("❌ Database Connection Error:", e)
    db = None
    cursor = None


# ==========================================
# 🔹 APPLICATION ROUTES
# ==========================================

# 🏠 HOME PAGE
@app.route("/")
def home():
    """Renders the main landing page of the application."""
    return render_template("home.html")


# 👤 YAJMAN BOOKING PAGE
@app.route("/yajman")
def yajman():
    """Renders the booking page dedicated for Yajmans."""
    return render_template("yajman_booking.html")


# 📿 BRAHMIN REGISTRATION PAGE
@app.route("/brahmin")
def brahmin():
    """
    Renders the Brahmin Verification / Registration page.
    Requires 'brahmin.html' to exist inside the templates directory.
    """
    return render_template("brahmin.html")


# 🚀 BRAHMIN VERIFICATION SUBMISSION HANDLER
@app.route("/brahmin_verify", methods=["POST"])
def brahmin_verify():
    """
    Handles form submission for Brahmin professional verification.
    Processes text inputs and uploaded multi-part document file names into the database.
    """
    if not db or not cursor:
        return "❌ Database connection is not active!", 500

    # Extracting text data from the verification form parameters
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    pathshala = request.form.get("pathshala")
    veda = request.form.get("veda")
    shakha = request.form.get("shakha")

    # Extracting target filenames from uploaded documents (Multipart form-data)
    marksheet10 = request.files.get("marksheet10").filename if request.files.get("marksheet10") else ""
    marksheet12 = request.files.get("marksheet12").filename if request.files.get("marksheet12") else ""
    certificate = request.files.get("certificate").filename if request.files.get("certificate") else ""
    aadhar = request.files.get("aadhar").filename if request.files.get("aadhar") else ""
    pan = request.files.get("pan").filename if request.files.get("pan") else ""
    photo = request.files.get("photo").filename if request.files.get("photo") else ""

    try:
        # Structured SQL query execution to prevent injection and persist data safely
        query = """
        INSERT INTO brahmins (name, mobile, pathshala, veda, shakha, marksheet10, marksheet12, certificate, aadhar, pan, photo) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, mobile, pathshala, veda, shakha, marksheet10, marksheet12, certificate, aadhar, pan, photo))
        db.commit()
        
        # Reloading page with a standardized dynamic success acknowledgement message
        return render_template("brahmin.html", result="✅ Verification Form Submitted Successfully!")
    except Exception as e:
        return f"❌ Error saving verification details: {e}", 500


# ==========================================
# 🔹 APPLICATION RUNNER
# ==========================================
if __name__ == "__main__":
    # Dynamically binds port provided by production environments like Render, defaulting locally to 5000.
    server_port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=server_port, debug=True)