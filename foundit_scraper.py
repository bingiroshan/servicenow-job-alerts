import requests
from bs4 import BeautifulSoup


def get_foundit_jobs():

    print("Checking Foundit jobs...")

    jobs_list = []

    url = "https://www.foundit.in/jobs/search?q=servicenow+administrator&where=hyderabad"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        print(
            f"Foundit Status Code: {response.status_code}"
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # FIND ALL JOB CARDS
        job_cards = soup.find_all("article")

        print(
            f"Foundit Job Cards Found: {len(job_cards)}"
        )

        for card in job_cards:

            try:

                # TITLE
                title_tag = card.find("h3")

                if not title_tag:
                    continue

                title = title_tag.text.strip()

                if len(title) < 5:
                    continue

                # LINK
                link_tag = card.find("a")

                if not link_tag:
                    continue

                link = link_tag.get(
                    "href",
                    ""
                )

                if not link.startswith("http"):

                    link = (
                        "https://www.foundit.in"
                        + link
                    )

                # COMPANY
                company = "Unknown"

                company_tag = card.find("span")

                if company_tag:

                    company_text = (
                        company_tag.text.strip()
                    )

                    if len(company_text) > 1:

                        company = company_text

                print(
                    "Foundit Job:",
                    title
                )

                jobs_list.append({

                    "title": title,

                    "company": company,

                    "link": link,

                    "platform": "Foundit"
                })

            except Exception as e:

                print(
                    "Foundit Parsing Error:",
                    e
                )

    except Exception as e:

        print("Foundit Error:", e)

    return jobs_list
