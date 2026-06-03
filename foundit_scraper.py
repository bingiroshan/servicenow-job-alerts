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

        # FIND ALL LINKS
        links = soup.find_all("a")

        print(
            f"Total Foundit Links Found: {len(links)}"
        )

        for link_tag in links:

            try:

                href = link_tag.get(
                    "href",
                    ""
                )

                text = link_tag.text.strip()

                # FILTER JOB LINKS
                if (
                    "/job/"
                    not in href.lower()
                ):

                    continue

                if len(text) < 5:
                    continue

                title = text

                if not href.startswith("http"):

                    href = (
                        "https://www.foundit.in"
                        + href
                    )

                print(
                    "Foundit Job:",
                    title
                )

                jobs_list.append({

                    "title": title,

                    "company": "Unknown",

                    "link": href,

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
