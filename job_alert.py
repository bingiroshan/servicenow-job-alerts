from filters import (
    is_duplicate,
    save_job,
    generate_job_id
)

from foundit_scraper import get_foundit_jobs

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
# PRODUCT BASED COMPANIES
# =========================

PRODUCT_BASED_COMPANIES = [

    "google",
    "microsoft",
    "amazon",
    "salesforce",
    "servicenow",
    "oracle",
    "adobe",
    "sap",
    "atlassian",
    "vmware",
    "intel",
    "paypal",
    "uber",
    "netflix",
    "apple",
    "meta",
    "ibm",
    "dell",
    "hp",
    "cisco",
    "linkedin",
    "jpmorgan",
    "goldman sachs",
    "wells fargo",
    "american express",
    "visa",
    "mastercard",
    "siemens",
    "sony",
    "nvidia",
    "qualcomm",
    "zoho",
    "freshworks",
    "intuit",
    "swiggy",
    "flipkart",
    "meesho",
    "razorpay",
    "paytm",
    "phonepe"
]


def is_product_company(company):

    company_lower = company.lower()

    return any(
        product_company in company_lower
        for product_company
        in PRODUCT_BASED_COMPANIES
    )

# =========================
# EXPERIENCE DETECTION
# =========================

def detect_experience(title):

    title_lower = title.lower()

    # HIGH EXPERIENCE
    high_experience_keywords = [

        "5+",
        "6+",
        "7+",
        "8+",
        "10+",

        "5 year",
        "6 year",
        "7 year",
        "8 year",
        "10 year",

        "senior",
        "lead",
        "architect",
        "principal"
    ]

    # MID EXPERIENCE
    mid_experience_keywords = [

        "2 year",
        "3 year",
        "4 year",

        "2+",
        "3+",
        "4+"
    ]

    # CHECK HIGH EXPERIENCE
    if any(
        keyword in title_lower
        for keyword in high_experience_keywords
    ):

        return "HIGH"

    # CHECK MID EXPERIENCE
    if any(
        keyword in title_lower
        for keyword in mid_experience_keywords
    ):

        return "MID"

    # DEFAULT
    return "UNKNOWN"

# =========================
# PRIORITY SCORING
# =========================

def calculate_priority(
    title,
    company
):

    score = 0

    title_lower = title.lower()

    # PRODUCT COMPANY BONUS
    if is_product_company(company):
        score += 5

    # SERVICENOW BONUS
    if "servicenow" in title_lower:
        score += 3

    # ADMIN BONUS
    if (
        "admin" in title_lower
        or
        "administrator" in title_lower
    ):
        score += 3

    # ITSM BONUS
    if "itsm" in title_lower:
        score += 2

    # EXPERIENCE BONUS
    experience_level = detect_experience(title)

    if experience_level == "MID":
        score += 3

    elif experience_level == "HIGH":
        score -= 5

    # FINAL PRIORITY
    if score >= 8:
        return "🔥 HIGH PRIORITY"

    elif score >= 5:
        return "⭐ MEDIUM PRIORITY"

    else:
        return "⚪ LOW PRIORITY"

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
# JOB FILTER
# =========================

def is_valid_job(title):

    title_lower = title.lower()

    allowed_keywords = [

        "servicenow",

        "servicenow administrator",

        "servicenow admin",

        "servicenow analyst",

        "servicenow developer",

        "itsm",

        "service desk",

        "incident",

        "platform",

        "admin",

        "developer"
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

        "staff engineer",

        "technical lead",

        "product owner",

        "12 year",

        "10 year",

        "9 year",

        "8 year",

        "7 year",

        "6 year",

        "5 year",

        "12+",

        "10+",

        "9+",

        "8+",

        "7+",

        "6+",

        "5+"
    ]

    # ALLOWED CHECK
    if not any(
        keyword in title_lower
        for keyword in allowed_keywords
    ):

        print("Skipped Irrelevant Role:", title)

        return False

    # BLOCKED CHECK
    if any(
        keyword in title_lower
        for keyword in blocked_keywords
    ):

        print("Skipped Senior/Remote Role:", title)

        return False

    return True

# =========================
# COMMON JOB PROCESSOR
# =========================

def process_job(
    title,
    company,
    link,
    platform
):

    global first_run

    clean_link = link.split("?")[0]

    # GENERATE UNIQUE JOB ID
    job_id = generate_job_id(
        title,
        company,
        platform
    )

    # DUPLICATE CHECK
    if is_duplicate(job_id):

        print("Duplicate Job Skipped")

        return

    # IGNORE OLD JOBS ON FIRST RUN
    if first_run:

        save_job(job_id)

        print("Old Job Ignored")

        return

    # PRODUCT COMPANY CHECK
    if is_product_company(company):

        company_type = "🔥 PRODUCT BASED COMPANY"

    else:

        company_type = "🏢 SERVICE BASED COMPANY"

    # PRIORITY SCORE
    priority = calculate_priority(
        title,
        company
    )

    # EXPERIENCE LEVEL
    experience_level = detect_experience(
        title
    )

    message = f"""
🚀 New ServiceNow Job Found

{priority}

{company_type}

📈 Experience Level: {experience_level}

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

    save_job(job_id)

# =========================
# LINKEDIN SCRAPER
# =========================

def check_linkedin_jobs():

    print("Checking LinkedIn jobs...")

    url = "https://www.linkedin.com/jobs/search/?keywords=ServiceNow&location=Hyderabad%2C%20Telangana%2C%20India"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
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

                title = job.find(
                    "h3"
                ).text.strip()

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
                print("LinkedIn Parsing Error:", e)

    except Exception as e:
        print("LinkedIn Error:", e)

# =========================
# FOUNDIT SCRAPER
# =========================

def check_foundit_jobs():

    print("Checking Foundit jobs...")

    try:

        foundit_jobs = get_foundit_jobs()

        print(
            f"Foundit Jobs Retrieved: {len(foundit_jobs)}"
        )

        for job in foundit_jobs:

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
                    "Foundit"
                )

            except Exception as e:
                print("Foundit Job Error:", e)

    except Exception as e:
        print("Foundit Error:", e)

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

    check_foundit_jobs()

    first_run = False

    time.sleep(1800)