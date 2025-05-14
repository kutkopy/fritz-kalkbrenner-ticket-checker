import requests
from bs4 import BeautifulSoup
from mailjet_rest import Client
import os

# Constants
CHECK_URL = "https://tickets.dasviertel.ch/"
TARGET_ARTIST = "Balkan"

# Environment variables from GitHub secrets
MAILJET_API_KEY = os.environ["MAILJET_API_KEY"]
MAILJET_API_SECRET = os.environ["MAILJET_API_SECRET"]
MAILJET_FROM_EMAIL = os.environ["MAILJET_FROM_MAIL"]
MAILJET_TO_EMAIL = os.environ["MAILJET_TO_MAIL"]

def check_tickets():
    response = requests.get(CHECK_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    return TARGET_ARTIST.lower() in soup.get_text().lower()

def send_email():
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": f"{MAILJET_FROM_EMAIL}",
                    "Name": "Ticket Agent"
                },
                "To": [
                    {
                        "Email": f"{MAILJET_TO_EMAIL}",
                        "Name": "You"
                    }
                ],
                "Subject": f"🎫 {TARGET_ARTIST} tickets available!",
                "TextPart": f"Tickets for {TARGET_ARTIST} are now available: {CHECK_URL}"
            }
        ]
    }
    print(f"Mail data:{data}")

    result = mailjet.send.create(data=data)
    print(f"Email sent. Status code: {result.status_code}")
    print(result.json())

if __name__ == "__main__":
    if check_tickets():
        print("✅ Tickets available")
        send_email()
    else:
        print("❌ No tickets available")
