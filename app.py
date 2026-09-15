from flask import Flask, render_template, request, redirect, url_for, send_file, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
from ai_model import analyze_skin_image
from pathlib import Path
import sqlite3


# ==================================================
# APP SETUP
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

app.secret_key = "dermalens-secret-key"


# ==================================================
# FOLDERS
# ==================================================

UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
REPORT_FOLDER = BASE_DIR / "reports"
DATABASE = BASE_DIR / "users.db"

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)


# ==================================================
# DATABASE
# ==================================================

def init_db():

    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


init_db()


# ==================================================
# ALLOWED FILE TYPES
# ==================================================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==================================================
# LOGIN REQUIRED
# ==================================================

def login_required():

    return "username" in session


# ==================================================
# SIGNUP
# ==================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return "Username and password are required."

        if len(password) < 6:
            return "Password must contain at least 6 characters."

        connection = sqlite3.connect(DATABASE)

        try:

            hashed_password = generate_password_hash(password)

            connection.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (username, hashed_password)
            )

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()
            return "Username already exists. Please login."

        connection.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        connection = sqlite3.connect(DATABASE)

        user = connection.execute(
            """
            SELECT username, password
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user[1], password):

            session["username"] = user[0]

            return redirect(url_for("home"))

        return "Invalid username or password."

    return render_template("login.html")


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    if not login_required():
        return redirect(url_for("login"))

    return render_template("index.html")


# ==================================================
# UPLOAD
# ==================================================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":

        if "image" not in request.files:
            return "No image selected."

        image = request.files["image"]

        if image.filename == "":
            return "No image selected."

        if not allowed_file(image.filename):
            return "Invalid image type."

        filename = secure_filename(image.filename)

        if filename == "":
            return "Invalid filename."

        image_path = UPLOAD_FOLDER / filename

        image.save(str(image_path))

        print("Image uploaded successfully:", filename)

        return redirect(
            url_for(
                "dashboard",
                image_name=filename
            )
        )

    return render_template("upload.html")


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
def dashboard():

    if not login_required():
        return redirect(url_for("login"))

    image_name = request.args.get("image_name")

    return render_template(
        "dashboard.html",
        image_name=image_name
    )


# ==================================================
# AI ANALYSIS
# ==================================================

@app.route("/analyze")
def analyze():

    if not login_required():
        return redirect(url_for("login"))

    image_name = request.args.get("image_name")

    if not image_name:
        return redirect(url_for("upload"))

    image_name = secure_filename(image_name)
    image_path = UPLOAD_FOLDER / image_name

    if not image_path.is_file():
        return "Image not found. Please upload again."

    analysis = analyze_skin_image(str(image_path))

    if not analysis.get("success"):
        return analysis.get(
            "error",
            "Unable to analyze image."
        )

    return render_template(
        "result.html",
        image_name=image_name,
        prediction=analysis.get(
            "prediction",
            "No prediction available"
        ),
        confidence=analysis.get(
            "confidence",
            0
        ),
        recommendation=analysis.get(
            "recommendation",
            "Please consult a qualified dermatologist."
        )
    )


# ==================================================
# RESULT
# ==================================================

@app.route("/result")
def result():

    if not login_required():
        return redirect(url_for("login"))

    image_name = request.args.get("image_name")

    if not image_name:
        return redirect(url_for("upload"))

    image_name = secure_filename(image_name)
    image_path = UPLOAD_FOLDER / image_name

    if not image_path.is_file():
        return "Image not found. Please upload again."

    analysis = analyze_skin_image(str(image_path))

    if not analysis.get("success"):
        return analysis.get(
            "error",
            "Unable to analyze image."
        )

    return render_template(
        "result.html",
        image_name=image_name,
        prediction=analysis.get(
            "prediction",
            "No prediction available"
        ),
        confidence=analysis.get(
            "confidence",
            0
        ),
        recommendation=analysis.get(
            "recommendation",
            "Please consult a qualified dermatologist."
        )
    )


# ==================================================
# PDF REPORT
# ==================================================

@app.route("/report")
def report():

    if not login_required():
        return redirect(url_for("login"))

    image_name = request.args.get("image_name")

    if not image_name:
        return "No image selected."

    image_name = secure_filename(image_name)
    image_path = UPLOAD_FOLDER / image_name

    if not image_path.is_file():
        return "Image not found. Please upload again."

    analysis = analyze_skin_image(str(image_path))

    prediction = analysis.get(
        "prediction",
        "No prediction available"
    )

    confidence = analysis.get(
        "confidence",
        0
    )

    recommendation = analysis.get(
        "recommendation",
        "Please consult a qualified dermatologist."
    )

    report_path = REPORT_FOLDER / "dermalens_report.pdf"

    pdf = canvas.Canvas(str(report_path))

    pdf.setTitle("DermaLens.AI Report")

    pdf.drawString(50, 800, "DermaLens.AI")

    pdf.drawString(
        50,
        770,
        "AI-Assisted Skin Image Analysis Report"
    )

    pdf.drawString(
        50,
        720,
        f"Username: {session.get('username', 'User')}"
    )

    pdf.drawString(
        50,
        690,
        f"Image: {image_name}"
    )

    pdf.drawString(
        50,
        650,
        f"AI Model Output: {prediction}"
    )

    pdf.drawString(
        50,
        610,
        f"Model Confidence: {confidence}%"
    )

    pdf.drawString(50, 560, "Recommendation:")

    pdf.drawString(
        50,
        535,
        recommendation[:100]
    )

    pdf.drawString(50, 480, "Medical Disclaimer:")

    pdf.drawString(
        50,
        455,
        "This is an AI-assisted research prototype."
    )

    pdf.drawString(
        50,
        435,
        "It is not a substitute for professional diagnosis."
    )

    pdf.drawString(
        50,
        415,
        "Please consult a qualified dermatologist."
    )

    pdf.save()

    print("PDF report generated successfully.")

    return send_file(
        str(report_path),
        as_attachment=True,
        download_name="dermalens_report.pdf"
    )


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    print("======================================")
    print("       DermaLens.AI is running!")
    print("======================================")
    print("Open: http://127.0.0.1:5000")
    print("======================================")

    app.run(debug=True)