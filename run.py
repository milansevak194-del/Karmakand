import os
import mysql.connector
from mysql.connector import pooling
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ==========================================
# 🔹 DATABASE CONFIGURATION & POOLING
# ==========================================
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'test')  # Default TiDB database is 'test'
DB_PORT = os.environ.get('DB_PORT', '3306')

# Configuration dictionary for MySQL connection
db_config = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "port": int(DB_PORT)
}

# If deploying on Render and using TiDB Cloud, force SSL connection safely
if 'DB_HOST' in os.environ and 'tidbcloud.com' in os.environ.get('DB_HOST', ''):
    db_config["ssl_verify_cert"] = True
    db_config["ssl_disabled"] = False

# Create a connection pool to manage auto-reconnects and prevent 500 server errors
try:
    db_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="karmakand_pool",
        pool_size=5,
        pool_reset_session=True,
        **db_config
    )
    print("✅ Database Connection Pool Created Successfully!")
    
    # Initialize tables upon setup
    db = db_pool.get_connection()
    cursor = db.cursor(dictionary=True)
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
    cursor.close()
    db.close()
    print("✅ Database Tables Verified and Synchronized Successfully!")
except mysql.connector.Error as e:
    print("❌ Database Connection Error during initialization:", e)
    db_pool = None

# Helper function to safely fetch an active database connection from the pool
def get_db_connection():
    if db_pool:
        return db_pool.get_connection()
    return None


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
    """Renders the Brahmin Verification / Registration page."""
    return render_template("brahmin_login.html")


# 🚀 BRAHMIN VERIFICATION SUBMISSION HANDLER
@app.route("/brahmin_verify", methods=["POST"])
def brahmin_verify():
    """Handles form submission for Brahmin professional verification with dynamic connection handling."""
    db = get_db_connection()
    if not db:
        return "❌ Database connection is not active!", 500

    cursor = db.cursor(dictionary=True)

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
    finally:
        # Safely close cursor and return connection back to the pool
        cursor.close()
        db.close()


# ==========================================
# 🔹 APPLICATION RUNNER
# ==========================================
if __name__ == "__main__":
    # Dynamically binds port provided by production environments like Render, defaulting locally to 5000.
    server_port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=server_port, debug=True)