from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def get_naukri_jobs():

    print("Checking Naukri jobs with Playwright...")

    jobs_list = []

    url = "https://www.naukri.com/servicenow-administrator-jobs-in-hyderabad"

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            page.wait_for_timeout(3000)

            html = page.content()

            browser.close()

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        jobs = soup.find_all(
            "div",
            class_="cust-job-tuple"
        )

        print(f"Naukri Jobs Found: {len(jobs)}")

        for job in jobs:

            try:

                title_tag = job.find(
                    "a",
                    class_="title"
                )

                company_tag = job.find(
                    "a",
                    class_="comp-name"
                )

                if not title_tag:
                    continue

                title = title_tag.text.strip()

                link = title_tag.get(
                    "href",
                    ""
                )

                if company_tag:
                    company = company_tag.text.strip()
                else:
                    company = "Unknown"

                print("Naukri Job:", title)

                jobs_list.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "platform": "Naukri"
                })

            except Exception as e:
                print("Naukri Parsing Error:", e)

    except Exception as e:
        print("Naukri Playwright Error:", e)

    return jobs_list
