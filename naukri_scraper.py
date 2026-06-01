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

        jobs = soup.find_all(
            "article",
            class_="jobTuple"
        )

        for job in jobs:

            try:

                title = job.find(
                    "a",
                    class_="title"
                ).text.strip()

                company = job.find(
                    "a",
                    class_="comp-name"
                ).text.strip()

                link = job.find(
                    "a",
                    class_="title"
                )["href"]

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
