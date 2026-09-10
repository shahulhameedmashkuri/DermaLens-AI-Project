# 🩺 DermaLens.AI

## AI-Assisted Skin Image Analysis System

DermaLens.AI is a web-based AI-assisted skin image analysis prototype built using Python and Flask. The application allows users to upload a skin image, process it through an analysis pipeline, view the analysis result, and download a PDF report.

> ⚠️ *Medical Disclaimer:* This project is an educational and research prototype. It is not a medical device and must not be used as a substitute for professional medical diagnosis, treatment, or advice.

---

## ✨ Features

* 📤 Upload skin images
* 🖼️ Display uploaded images on an analysis dashboard
* 🔬 AI-assisted prototype analysis pipeline
* 📊 Prediction result display
* 🎯 Confidence score display
* 💡 Recommendation section
* 📄 Downloadable PDF analysis report
* 🔒 Secure filename handling
* 🛡️ Basic file type validation
* 📱 Responsive web interface

---

## 🛠️ Technologies Used

* *Python*
* *Flask*
* *HTML5*
* *CSS3*
* *Pillow*
* *ReportLab*

---

## 📂 Project Structure

text
DermaLens.AI/
│
├── app.py
├── ai_model.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── dashboard.html
│   └── result.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/
│       └── .gitkeep
│
└── reports/
    └── .gitkeep


---

## ⚙️ Installation

### 1. Clone the repository

bash
git clone <your-repository-url>
cd DermaLens.AI


### 2. Create a virtual environment (recommended)

bash
python -m venv venv


### 3. Activate the virtual environment

*Windows*

bash
venv\Scripts\activate


*macOS/Linux*

bash
source venv/bin/activate


### 4. Install dependencies

bash
pip install -r requirements.txt


---

## ▶️ Run the Application

### Local Development

Start the Flask application:

```bash
python app.py


---

## 🔄 Application Workflow

text
Upload Skin Image
        ↓
Secure File Validation
        ↓
Image Storage
        ↓
AI-Assisted Analysis Pipeline
        ↓
Prediction & Confidence Result
        ↓
Recommendation
        ↓
PDF Report Generation


---

## 🧠 AI Analysis Module

The current version contains a prototype AI analysis module designed to demonstrate the complete application workflow.

The project architecture allows a trained and appropriately validated machine-learning model to be integrated into ai_model.py in the future.

Current prototype output includes:

* Prediction status
* Confidence value
* Recommendation

---

## 🚀 Future Improvements

* Integration of a trained and validated dermatology image classification model
* Improved image preprocessing
* Multiple skin condition classification
* Model confidence visualization
* User authentication
* Analysis history
* Database integration
* Cloud deployment
* Advanced PDF reports
* Mobile optimization

---

## ⚠️ Disclaimer

DermaLens.AI is an AI-assisted educational prototype.

The analysis output should *not* be considered a medical diagnosis. Users should always consult a qualified healthcare professional or dermatologist for medical concerns.

---

## 👨‍💻 Developer

*Shaik Shahul Hameed Mashkuri*

B.Tech — Artificial Intelligence & Data Science

---

## ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.