SEEN_JOBS_FILE = "seen_jobs.txt"

# Load already seen jobs

try:

    with open(
        SEEN_JOBS_FILE,
        "r"
    ) as file:

        seen_jobs = set(
            file.read().splitlines()
        )

except FileNotFoundError:

    seen_jobs = set()


def is_duplicate(link):

    return link in seen_jobs


def save_job(link):

    seen_jobs.add(link)

    with open(
        SEEN_JOBS_FILE,
        "a"
    ) as file:

        file.write(link + "\n")