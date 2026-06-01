from filters import is_duplicate, save_job
from naukri_scraper import get_naukri_jobs
import requests
from bs4 import BeautifulSoup
import time
import smtplib
import os

from email.mime.text import MIMEText

# =========================
# FIRST RUN CONTROL
# =========================

first_run = True

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
# TELEGRAM FUNCTION
# =========================

def send_telegram_message(message):

    try:

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(
            telegram_url,
            data=payload
        )

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

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            TO_EMAIL,
            msg.as_string()
        )

        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print(f"Email Error: {e}")

# =========================
# JOB SCRAPER
# =========================

def check_jobs():

    global first_run

    print("Checking jobs...")

    url = "https://www.linkedin.com/jobs/search/?keywords=ServiceNow%20Administrator&location=Hyderabad%2C%20Telangana%2C%20India"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    jobs = soup.find_all(
        "div",
        class_="base-card"
    )

    if not jobs:
        print("No jobs found")

    for job in jobs:

        try:

            title = job.find("h3").text.strip()

            title_lower = title.lower()

            # =========================
            # ALLOWED ROLE KEYWORDS
            # =========================

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

            # =========================
            # BLOCK SENIOR/REMOTE
            # =========================

            blocked_keywords = [
                "senior",
                "lead",
                "manager",
                "architect",
                "principal",
                "director",
                "consultant",
                "remote",
                "offshore",
                "usa",
                "uk",
                "canada",
                "europe",
                "singapore",
                "australia"
            ]

            # =========================
            # EXPERIENCE FILTER
            # =========================

            blocked_experience = [
                "5 year",
                "5+",
                "6 year",
                "6+",
                "7 year",
                "7+",
                "8 year",
                "8+",
                "10+"
            ]

            # =========================
            # SKIP IRRELEVANT ROLES
            # =========================

            if not any(
                keyword in title_lower
                for keyword in allowed_keywords
            ):

                print(
                    "Skipped Irrelevant Role:",
                    title
                )

                continue

            # =========================
            # SKIP SENIOR/REMOTE ROLES
            # =========================

            if any(
                keyword in title_lower
                for keyword in blocked_keywords
            ):

                print(
                    "Skipped Senior/Remote Role:",
                    title
                )

                continue

            # =========================
            # SKIP 5+ YEARS ROLES
            # =========================

            if any(
                keyword in title_lower
                for keyword in blocked_experience
            ):

                print(
                    "Skipped High Experience Role:",
                    title
                )

                continue

            company = job.find(
                "h4"
            ).text.strip()

            link = job.find(
                "a"
            )["href"]

            # Remove LinkedIn tracking params
            clean_link = link.split("?")[0]

            message = f"""
🎉 New ServiceNow Job Found

💼 Title: {title}

🏢 Company: {company}

🔗 Apply Here:
{clean_link}
"""

            # =========================
            # DUPLICATE CHECK
            # =========================

            if is_duplicate(clean_link):

                print("Duplicate Job Skipped")

                continue

            # =========================
            # FIRST STARTUP
            # IGNORE OLD JOBS
            # =========================

            if first_run:

                save_job(clean_link)

                print("Old Job Ignored")

                continue

            print(message)

            send_telegram_message(message)

            send_email(
                "New ServiceNow Job Alert",
                message
            )

            save_job(clean_link)

        except Exception as e:

            print("Error:", e)

    # =========================
    # FIRST RUN COMPLETE
    # =========================

    first_run = False

# =========================
# MAIN LOOP
# =========================

print(
    "ServiceNow Job Bot Started Successfully"
)

send_telegram_message(
    "✅ ServiceNow Job Bot Started Successfully"
)

while True:

    check_jobs()

    time.sleep(1800)

