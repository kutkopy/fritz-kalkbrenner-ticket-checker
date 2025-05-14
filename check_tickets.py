import requests
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

CHECK_URL = "https://tickets.dasviertel.ch/"
TARGET_ARTIST = "Balkan"
TO_EMAIL = os.environ["TO_EMAIL"]
FROM_EMAIL = os.environ["FROM_EMAIL"]  # e.g. verified sender on SendGrid
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

def check_tickets():
    response = requests.get(CHECK_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    return TARGET_ARTIST.lower() in soup.get_text().lower()

def send_email():
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject=f"🎫 {TARGET_ARTIST} tickets available!",
        plain_text_content=f"Tickets available at {CHECK_URL}"
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent. Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    if check_tickets():
        send_email()
