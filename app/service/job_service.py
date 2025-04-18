from app.service.resume_processor import process_resume
from app.service.job_search import search_jobs
from app.service.job_ranking import rank_jobs_with_gemini
from app.service.resume_optimizer import optimize_resume_for_jobs
from app.service.data_formater import generate_final_api_response
import json

def process_resume_and_find_jobs(resume_path, job_profile):
    user_info = process_resume(resume_path)
    job_openings = search_jobs(job_profile, user_info["Experience"])
    top_5_jobs = rank_jobs_with_gemini(user_info, job_openings)[:5]
    optimized_user_data = optimize_resume_for_jobs(user_info, top_5_jobs)
    final_response = generate_final_api_response(user_info, top_5_jobs, optimized_user_data)
    print(json.dumps(final_response, indent=4))
    return final_response