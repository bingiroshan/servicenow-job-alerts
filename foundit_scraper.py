import requests
from bs4 import BeautifulSoup


def get_foundit_jobs():

    print("Checking Foundit jobs...")

    jobs_list = []

    url = "https://www.foundit.in/srp/results?query=servicenow%20administrator&locations=Hyderabad"

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
            class_="cardContainer"
        )

        print(f"Foundit Jobs Found: {len(jobs)}")

        for job in jobs:

            try:

                title_tag = job.find(
                    "div",
                    class_="jobTitle"
                )

                company_tag = job.find(
                    "div",
                    class_="companyName"
                )

                link_tag = job.find("a")

                if not title_tag or not link_tag:
                    continue

                title = title_tag.text.strip()

                if company_tag:
                    company = company_tag.text.strip()
                else:
                    company = "Unknown"

                link = link_tag.get(
                    "href",
                    ""
                )

                if not link.startswith("http"):
                    link = (
                        "https://www.foundit.in"
                        + link
                    )

                print("Foundit Job:", title)

                jobs_list.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "platform": "Foundit"
                })

            except Exception as e:
                print("Foundit Parsing Error:", e)

    except Exception as e:
        print("Foundit Error:", e)

    return jobs_list