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

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        jobs = soup.find_all("div", class_="srp-jobtuple-wrapper")

        print(f"Naukri Jobs Found: {len(jobs)}")

        for job in jobs:

            try:

                title_tag = job.find("a", class_="title")

                company_tag = job.find(
                    "a",
                    class_="comp-name"
                )

                if not title_tag or not company_tag:
                    continue

                title = title_tag.text.strip()

                company = company_tag.text.strip()

                link = title_tag["href"]

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
