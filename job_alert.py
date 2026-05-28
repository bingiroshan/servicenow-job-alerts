import requests
from bs4 import BeautifulSoup
import telegram
import time
import os
import smtplib
from email.mime.text import MIMEText

# =========================
# ENVIRONMENT VARIABLES
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# =========================
# TELEGRAM SETUP
# =========================

bot = telegram.Bot(token=BOT_TOKEN)

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
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

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

    for job in jobs[:10]:

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
    "5+"
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

            unique_job = title + company

            if unique_job not in seen_jobs:

                seen_jobs.add(unique_job)

                job_message = f"""
🚨 New ServiceNow Job Found

💼 Title: {title}

🏢 Company: {company}

🔗 Apply Here:
{link}
"""

                print(job_message)

                # Telegram Alert
                send_telegram_message(job_message)

                # Email Alert
                send_email(
                    "New ServiceNow Job Found",
                    job_message
                )

        except Exception as e:
            print(f"Job Parse Error: {e}")

# =========================
# MAIN LOOP
# =========================

print("ServiceNow Job Bot Started Successfully")

send_telegram_message("✅ ServiceNow Job Bot Started Successfully")

while True:

    try:
        check_jobs()

    except Exception as e:
        error_message = f"Bot Error: {e}"
        print(error_message)

    print("Sleeping for 1 hour...")

    time.sleep(3600)