from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

EMAIL_ADDRESS = "confirmationpin@gmail.com"
EMAIL_PASSWORD = "dtij stiy nwmf xrqk"

@app.route("/")
def form():
return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
data = request.form
id_card = request.files["id_card"]
passport = request.files["passport"]

msg = EmailMessage()
msg["Subject"] = "New Application Form Submission"
msg["From"] = EMAIL_ADDRESS
msg["To"] = EMAIL_ADDRESS

msg.set_content(f"""
FULL NAME: {data['fullname']}
EMAIL: {data['email']}
PHONE: {data['phone']}
GENDER: {data['gender']}
DATE OF BIRTH: {data['dob']}
NATIONALITY: {data['nationality']}
STATE: {data['state']}
CITY: {data['city']}
ADDRESS: {data['address']}
OCCUPATION: {data['occupation']}
MARITAL STATUS: {data['marital_status']}
NEXT OF KIN NAME: {data['nok_name']}
NEXT OF KIN PHONE: {data['nok_phone']}
REASON: {data['reason']}
""")

# Attach ID card
msg.add_attachment(
id_card.read(),
maintype="application",
subtype="octet-stream",
filename=id_card.filename
)

# Attach Passport
msg.add_attachment(
passport.read(),
maintype="application",
subtype="octet-stream",
filename=passport.filename
)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
smtp.send_message(msg)

return "Form submitted successfully!"

if __name__ == "__main__":
app.run(debug=True)
