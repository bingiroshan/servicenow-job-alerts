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

        jobs = soup.find_all("div")

        print(
            f"Total Foundit Divs Found: {len(jobs)}"
        )

        for job in jobs:

            try:

                title_tag = job.find("h3")

                link_tag = job.find("a")

                if not title_tag:
                    continue

                if not link_tag:
                    continue

                title = title_tag.text.strip()

                link = link_tag.get(
                    "href",
                    ""
                )

                if not link.startswith("http"):

                    link = (
                        "https://www.foundit.in"
                        + link
                    )

                company = "Unknown"

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