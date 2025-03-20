import aiosmtplib
from email.message import EmailMessage

import os

SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT") 
async def send_confirmation_email(email: str, url: str):
    msg = EmailMessage()
    msg["Subject"] = "Confirm your Email"
    msg["From"] = SMTP_USERNAME
    msg["To"] = email
    msg.set_content(f"Click the link to confirm your email {url}")

    await aiosmtplib.send(msg,
                           hostname=SMTP_SERVER, 
                           port=SMTP_PORT,
                             username=SMTP_USERNAME,
                               password=SMTP_PASSWORD,
                                 start_tls=True)