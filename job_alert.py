import requests
from bs4 import BeautifulSoup
import time
import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================
# TELEGRAM CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# EMAIL CONFIG
# =========================

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# =========================
# TRACK SEEN JOBS
# =========================

seen_jobs = set()

# =========================
# TELEGRAM FUNCTION
# =========================

def send_telegram_message(message):

    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(telegram_url, data=payload)

        if response.status_code == 200:
            print("Telegram message sent successfully")
        else:
            print("Telegram API Error:", response.text)

    except Exception as e:
        print(f"Telegram Error: {e}")

# =========================
# EMAIL FUNCTION
# =========================

def send_email(subject, body):

    try:
        msg = MIMEMultipart()

        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print(f"Email Error: {e}")

# =========================
# JOB SCRAPER
# =========================

def check_jobs():

    print("Checking jobs...")

    url = "https://www.linkedin.com/jobs/search/?keywords=ServiceNow%20Administrator&location=Hyderabad%2C%20Telangana%2C%20India"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("div", class_="base-card")

    if not jobs:
        print("No jobs found")

    for job in jobs:

        try:
            title = job.find("h3").text.strip()

            title_lower = title.lower()

            # Relevant roles for your profile
            allowed_keywords = [
                "servicenow administrator",
                "servicenow admin",
                "servicenow analyst",
                "itsm",
                "incident",
                "support",
                "service desk",
                "administrator",
                "analyst"
            ]

            # Skip senior/high experience roles
            blocked_keywords = [
                "senior",
                "lead",
                "manager",
                "architect",
                "principal",
                "director",
                "consultant",
                "10+",
                "8+",
                "7+",
                "6+",
                "5+",
                "remote",
                "offshore",
                "usa",
                "uk",
                "canada",
                "europe",
                "singapore",
                "australia"

                  
            ]

            # Allow only relevant roles
            if not any(keyword in title_lower for keyword in allowed_keywords):
                print("Skipped Irrelevant Role:", title)
                continue

            # Skip senior roles
            if any(keyword in title_lower for keyword in blocked_keywords):
                print("Skipped Senior Role:", title)
                continue

            company = job.find("h4").text.strip()

            link = job.find("a")["href"]

            message = f"""
🎉 New ServiceNow Job Found

💼 Title: {title}

🏢 Company: {company}

🔗 Apply Here:
{link}
"""

            if link not in seen_jobs:

                print(message)

                send_telegram_message(message)

                send_email(
                    "New ServiceNow Job Alert",
                    message
                )

                seen_jobs.add(link)

        except Exception as e:
            print("Error:", e)

# =========================
# MAIN LOOP
# =========================

print("ServiceNow Job Bot Started Successfully")

send_telegram_message(
    "✅ ServiceNow Job Bot Started Successfully"
)

while True:

    check_jobs()

    time.sleep(1800)
