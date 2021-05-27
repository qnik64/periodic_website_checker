import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from gmail_credentials import *
from script_logger import script_log


def send_email(receiver, subject, message):
    port = 465

    full_message = MIMEMultipart("alternative")
    full_message["Subject"] = subject
    full_message["From"] = GMAIL_ADDRESS
    full_message["To"] = receiver
    full_message.attach(MIMEText(message, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(GMAIL_ADDRESS, GMAIL_PASSWD)
        server.sendmail(GMAIL_ADDRESS, receiver, full_message.as_string())
    script_log("e-mail sent")
