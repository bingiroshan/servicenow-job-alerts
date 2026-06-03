import hashlib

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


# =========================
# CREATE UNIQUE JOB ID
# =========================

def generate_job_id(
    title,
    company,
    platform
):

    unique_string = (
        f"{title.lower()}|"
        f"{company.lower()}|"
        f"{platform.lower()}"
    )

    return hashlib.md5(
        unique_string.encode()
    ).hexdigest()


# =========================
# DUPLICATE CHECK
# =========================

def is_duplicate(job_id):

    return job_id in seen_jobs


# =========================
# SAVE JOB
# =========================

def save_job(job_id):

    seen_jobs.add(job_id)

    with open(
        SEEN_JOBS_FILE,
        "a"
    ) as file:

        file.write(job_id + "\n")
