import requests
from bs4 import BeautifulSoup
from mailjet_rest import Client
import os

# Constants
CHECK_URL = "https://tickets.dasviertel.ch/"
TARGET_ARTIST = "Fritz Kalkbrenner"

# Environment variables from GitHub secrets
MAILJET_API_KEY = os.environ["MAILJET_API_KEY"]
MAILJET_API_SECRET = os.environ["MAILJET_API_SECRET"]
FROM_EMAIL = os.environ["FROM_EMAIL"]
TO_EMAIL = os.environ["TO_EMAIL"]

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
                    "Email": FROM_EMAIL,
                    "Name": "Ticket Agent"
                },
                "To": [
                    {
                        "Email": TO_EMAIL,
                        "Name": "You"
                    }
                ],
                "Subject": "🎫 Fritz Kalkbrenner tickets available!",
                "TextPart": f"Tickets for {TARGET_ARTIST} are now available: {CHECK_URL}"
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(f"Email sent. Status code: {result.status_code}")
    print(result.json())

if __name__ == "__main__":
    if check_tickets():
        send_email()
