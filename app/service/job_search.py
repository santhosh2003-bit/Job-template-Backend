# import requests
# import json
#
# # Constants
# API_TOKEN = 'apify_api_VjwuTGLTIjbkqihsb1RWPRTUroM6Pb3P4cLw'  # Replace with your actual token
# API_URL = f'https://api.apify.com/v2/acts/bebity~linkedin-jobs-scraper/run-sync-get-dataset-items?token={API_TOKEN}&memory=128'
#
#
# def search_jobs(job_title, experience_level=3, rows=10):
#     """
#     Fetches job listings from LinkedIn Jobs Scraper API.
#
#     Args:
#         job_title (str): Title of the job to search for.
#         experience_level (int): User's experience level (in years).
#         rows (int): Number of job listings to fetch.
#
#     Returns:
#         list: A list of job dictionaries with relevant information.
#     """
#     payload = {
#         "experienceLevel": str(experience_level),
#         "proxy": {
#             "useApifyProxy": "true",
#             "apifyProxyGroups": ["RESIDENTIAL"]
#         },
#         "rows": rows,
#         "title": job_title
#     }
#
#     try:
#         # Request to run the actor and get the dataset
#         response = requests.post(API_URL, json=payload)
#         response.raise_for_status()
#
#         # Parse the response data
#         data = response.json()
#
#         # Extract useful job information
#         # job_listings = [
#         #     {
#         #         "title": job.get("title"),
#         #         "company": job.get("company"),
#         #         "location": job.get("location"),
#         #         "url": job.get("jobUrl")
#         #     }
#         #     for job in data if job.get("title") and job.get("jobUrl")
#         # ]
#
#         return data
#
#     except requests.RequestException as e:
#         print(f"Error fetching job listings: {e}")
#         return []
#     except json.JSONDecodeError:
#         print("Error decoding JSON response.")
#         return []


import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters, SalaryBaseFilters

# Minimal logging configuration (only errors)
logging.basicConfig(level=logging.ERROR)

# Global lists to store job results and raw job data
job_results = []

EXPERIENCE_MAPPING = {
    "0": ExperienceLevelFilters.ENTRY_LEVEL,   # 0 years → Entry Level
    "1": ExperienceLevelFilters.ENTRY_LEVEL,   # 1 year → Entry Level
    "2": ExperienceLevelFilters.MID_SENIOR,    # 2 years → Mid-Senior
    "3": ExperienceLevelFilters.MID_SENIOR,    # 3 years → Mid-Senior
    "4": ExperienceLevelFilters.DIRECTOR,      # 4 years → Director
    "5": ExperienceLevelFilters.DIRECTOR,      # 5 years → Director
    "6": ExperienceLevelFilters.EXECUTIVE      # 6+ years → Executive
}


def process_job_data(data: EventData):
    """
    Process a job event:
    - Store the full raw data in raw_job_data.
    - Build and store a formatted dictionary in job_results.
    """

    # Build a formatted job dictionary with selected fields
    job_info = {
        "title": data.title,
        "company": data.company,
        "location": data.location,
        "place": data.place,
        "job_url": data.link,
        "apply_link": getattr(data, "apply_link", None),
        "date": data.date,
        "job_description": data.description,
        "job_id": data.job_id,
    }
    job_results.append(job_info)

def search_jobs(job_profile, experience):
    """
    Scrape jobs based on job profile and experience level.
    """
    experience_filter = EXPERIENCE_MAPPING.get(experience, ExperienceLevelFilters.EXECUTIVE)

    scraper = LinkedinScraper(
        chrome_executable_path=None,
        chrome_binary_location=None,
        chrome_options=None,
        headless=True,
        max_workers=1,
        slow_mo=0.5,
        page_load_timeout=40
    )

    scraper.on(Events.DATA, process_job_data)

    query = Query(
        query=job_profile,
        options=QueryOptions(
            locations=['India'],
            apply_link=True,
            skip_promoted_jobs=True,
            limit=10,
            filters=QueryFilters(
                time=TimeFilters.WEEK,
                experience=experience_filter
            )
        )
    )

    try:
        scraper.run([query])
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

    # Check if job_results is empty
    if not job_results:
        print("No jobs found.")
        return []

    return job_results


# def search_jobs(job_profile, experience):
    """
    Scrape jobs based on job profile and experience level.
    """

    # Get the experience level filter based on years of experience
    experience_filter = EXPERIENCE_MAPPING.get(experience, ExperienceLevelFilters.EXECUTIVE)

    # Initialize the scraper
    scraper = LinkedinScraper(
        chrome_executable_path=None,
        chrome_binary_location=None,
        chrome_options=None,
        headless=True,
        max_workers=1,
        slow_mo=0.5,
        page_load_timeout=40
    )

    # Register the event handler for job data
    scraper.on(Events.DATA, process_job_data)

    # Define the query
    query = Query(
        query=job_profile,
        options=QueryOptions(
            locations=['India'],
            apply_link=True,
            skip_promoted_jobs=True,
            limit=10,
            filters=QueryFilters(
                time=TimeFilters.WEEK,
                experience=experience_filter
            )
        )
    )

    # Run the scraper with the query (blocking call)
    scraper.run([query])

    return job_results