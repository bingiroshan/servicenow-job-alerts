import requests
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot
import time

# ==========================
# TELEGRAM CONFIG
# ==========================

BOT_TOKEN = "8706896578:AAFPGOrW7BIVqrGlwh0eUzrFM7p8ILvPBdg"
CHAT_ID = "1077832381"

bot = Bot(token=BOT_TOKEN)

# Store sent jobs
sent_jobs = set()

# ==========================
# JOB URLS
# ==========================

urls = [
    "https://www.naukri.com/servicenow-administrator-jobs-in-hyderabad-2-to-5-years",
    "https://in.indeed.com/jobs?q=servicenow+administrator&l=Hyderabad",
    "https://www.foundit.in/srp/results?query=ServiceNow%20Administrator&locations=Hyderabad"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ==========================
# SEND TELEGRAM MESSAGE
# ==========================

async def send_telegram_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

# ==========================
# CHECK JOBS
# ==========================

def check_jobs():

    for url in urls:

        try:

            response = requests.get(url, headers=headers, timeout=20)

            soup = BeautifulSoup(response.text, "lxml")

            links = soup.find_all("a")

            for link in links:

                title = link.get_text(strip=True)
                href = link.get("href")

                if not href:
                    continue

                keywords = [
                    "servicenow",
                    "administrator",
                    "admin",
                    "itsm"
                ]

                if any(word in title.lower() for word in keywords):

                    unique_job = title + href

                    if unique_job not in sent_jobs:

                        sent_jobs.add(unique_job)

                        message = f"""
🚨 New ServiceNow Job

📌 {title}

🔗 Apply Here:
{href}
"""

                        asyncio.run(
                            send_telegram_message(message)
                        )

                        print("Alert Sent")

        except Exception as e:

            print("Error:", e)

# ==========================
# MAIN
# ==========================

print("Job Alert Bot Started...")

asyncio.run(
    send_telegram_message(
        "✅ ServiceNow Job Bot Started Successfully"
    )
)

while True:

    check_jobs()

    print("Checking jobs...")

    time.sleep(600)