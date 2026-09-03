from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas
from ai_model import analyze_skin_image
import os


# ==================================================
# APP SETUP
# ==================================================

app = Flask(__name__)


# ==================================================
# FOLDERS
# ==================================================

UPLOAD_FOLDER = "static/uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


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
# HOME
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# UPLOAD
# ==================================================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        # Check image field
        if "image" not in request.files:
            return "No image selected"

        image = request.files["image"]

        # Check filename
        if image.filename == "":
            return "No image selected"

        # Check extension
        if not allowed_file(image.filename):
            return (
                "Invalid image type. "
                "Please upload PNG, JPG, JPEG or WEBP."
            )

        # Secure filename
        filename = secure_filename(image.filename)

        if filename == "":
            return "Invalid filename"

        # Image save path
        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        # Save image
        image.save(image_path)

        print("Image uploaded successfully:", filename)

        # Redirect to dashboard
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

    image_name = request.args.get("image_name")

    # Check image name
    if not image_name:
        return redirect(
            url_for("upload")
        )

    # Secure filename
    image_name = secure_filename(image_name)

    # Image path
    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image_name
    )

    # Check image exists
    if not os.path.isfile(image_path):

        return (
            "Image not found. "
            "Please upload the image again."
        )

    # ===============================================
    # AI ANALYSIS
    # ===============================================

    analysis = analyze_skin_image(
        image_path
    )

    # Check analysis success
    if not analysis.get("success"):

        return analysis.get(
            "error",
            "Unable to analyze image."
        )

    # Show result
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

    image_name = request.args.get("image_name")

    # Check image
    if not image_name:

        return redirect(
            url_for("upload")
        )

    # Secure filename
    image_name = secure_filename(image_name)

    # Image path
    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image_name
    )

    # Check image exists
    if not os.path.isfile(image_path):

        return (
            "Image not found. "
            "Please upload the image again."
        )

    # Run analysis
    analysis = analyze_skin_image(
        image_path
    )

    # Check success
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

    image_name = request.args.get("image_name")

    # Check image name
    if not image_name:

        return "No image selected"

    # Secure filename
    image_name = secure_filename(image_name)

    # Image path
    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image_name
    )

    # Check image exists
    if not os.path.isfile(image_path):

        return (
            "Image not found. "
            "Please upload the image again."
        )

    # Run analysis again for report
    analysis = analyze_skin_image(
        image_path
    )

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

    # PDF filename
    report_filename = "dermalens_report.pdf"

    report_path = os.path.join(
        REPORT_FOLDER,
        report_filename
    )

    # Create PDF
    pdf = canvas.Canvas(
        report_path
    )

    pdf.setTitle(
        "DermaLens.AI Report"
    )

    # Title
    pdf.drawString(
        50,
        800,
        "DermaLens.AI"
    )

    pdf.drawString(
        50,
        770,
        "AI-Assisted Skin Image Analysis Report"
    )

    # Image
    pdf.drawString(
        50,
        720,
        f"Image: {image_name}"
    )

    # Prediction
    pdf.drawString(
        50,
        680,
        f"Prediction: {prediction}"
    )

    # Confidence
    pdf.drawString(
        50,
        640,
        f"Confidence: {confidence}%"
    )

    # Recommendation
    pdf.drawString(
        50,
        600,
        "Recommendation:"
    )

    pdf.drawString(
        50,
        580,
        recommendation
    )

    # Disclaimer
    pdf.drawString(
        50,
        520,
        "Medical Disclaimer:"
    )

    pdf.drawString(
        50,
        490,
        "DermaLens.AI is an AI-assisted prototype and is not"
    )

    pdf.drawString(
        50,
        470,
        "a substitute for professional medical diagnosis."
    )

    # Save PDF
    pdf.save()

    print(
        "PDF report generated successfully."
    )

    # Download PDF
    return send_file(
        report_path,
        as_attachment=True,
        download_name="dermalens_report.pdf"
    )


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    print("")
    print("======================================")
    print("       DermaLens.AI is running!")
    print("======================================")
    print("Open this URL in your browser:")
    print("http://127.0.0.1:5000")
    print("======================================")
    print("")

    app.run(
        debug=True
    )