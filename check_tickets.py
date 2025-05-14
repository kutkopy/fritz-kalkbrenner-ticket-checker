import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import os

CHECK_URL = "https://tickets.dasviertel.ch/"
TARGET_ARTIST = "Balkan Comedy Night"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
YOUR_EMAIL = os.environ["YOUR_EMAIL"]

def check_tickets():
    response = requests.get(CHECK_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    return TARGET_ARTIST.lower() in soup.get_text().lower()

def send_email():
    msg = EmailMessage()
    msg['Subject'] = f"🎫 {TARGET_ARTIST} tickets available!"
    msg['From'] = SMTP_USER
    msg['To'] = YOUR_EMAIL
    msg.set_content(f"Check the ticket page: {CHECK_URL}")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    if check_tickets():
        send_email()
