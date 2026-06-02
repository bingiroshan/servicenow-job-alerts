import requests
from bs4 import BeautifulSoup


def get_naukri_jobs():

    print("Checking Naukri jobs...")

    jobs_list = []

    url = "https://www.naukri.com/servicenow-administrator-jobs-in-hyderabad"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers
        )

        print("Naukri Status Code:", response.status_code)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        jobs = soup.find_all("article")

        print("Total Article Tags Found:", len(jobs))

        for job in jobs:

            try:

                title_tag = job.find("a")

                if not title_tag:
                    continue

                title = title_tag.text.strip()

                link = title_tag.get("href", "")

                company_tag = job.find("a", class_="comp-name")

                if company_tag:
                    company = company_tag.text.strip()
                else:
                    company = "Unknown"

                print("Naukri Job Found:", title)

                jobs_list.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "platform": "Naukri"
                })

            except Exception as e:
                print("Naukri Parsing Error:", e)

    except Exception as e:
        print("Naukri Error:", e)

    return jobs_list
