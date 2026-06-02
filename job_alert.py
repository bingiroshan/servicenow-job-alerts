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
# COMMON JOB FILTER
# =========================

def is_valid_job(title):

    title_lower = title.lower()

    allowed_keywords = [
        "servicenow administrator",
        "servicenow admin",
        "servicenow analyst",
        "itsm",
        "service desk",
        "incident"
    ]

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
        "australia",
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

    if not any(
        keyword in title_lower
        for keyword in allowed_keywords
    ):

        print("Skipped Irrelevant Role:", title)

        return False

    if any(
        keyword in title_lower
        for keyword in blocked_keywords
    ):

        print("Skipped Senior/Remote Role:", title)

        return False

    return True

# =========================
# PROCESS JOB
# =========================

def process_job(
    title,
    company,
    link,
    platform
):

    global first_run

    clean_link = link.split("?")[0]

    # Duplicate Check
    if is_duplicate(clean_link):

        print("Duplicate Job Skipped")

        return

    # Ignore old jobs during first startup
    if first_run:

        save_job(clean_link)

        print("Old Job Ignored")

        return

    message = f"""
🚀 New ServiceNow Job Found

🌐 Platform: {platform}

💼 Title: {title}

🏢 Company: {company}

🔗 Apply Here:
{clean_link}
"""

    print(message)

    send_telegram_message(message)

    send_email(
        "New ServiceNow Job Alert",
        message
    )

    save_job(clean_link)

# =========================
# LINKEDIN JOBS
# =========================

def check_linkedin_jobs():

    print("Checking LinkedIn jobs...")

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

    print(f"LinkedIn Jobs Found: {len(jobs)}")

    for job in jobs:

        try:

            title = job.find("h3").text.strip()

            if not is_valid_job(title):
                continue

            company = job.find(
                "h4"
            ).text.strip()

            link = job.find(
                "a"
            )["href"]

            process_job(
                title,
                company,
                link,
                "LinkedIn"
            )

        except Exception as e:
            print("LinkedIn Error:", e)

# =========================
# NAUKRI JOBS
# =========================

def check_naukri_jobs():

    print("Checking Naukri jobs...")

    naukri_jobs = get_naukri_jobs()

    print(f"Naukri Jobs Retrieved: {len(naukri_jobs)}")

    for job in naukri_jobs:

        try:

            title = job["title"]

            if not is_valid_job(title):
                continue

            company = job["company"]

            link = job["link"]

            process_job(
                title,
                company,
                link,
                "Naukri"
            )

        except Exception as e:
            print("Naukri Error:", e)

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

    check_linkedin_jobs()

    check_naukri_jobs()

    first_run = False

    time.sleep(1800)

