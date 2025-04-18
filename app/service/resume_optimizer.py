import json
import re
from langchain import PromptTemplate, LLMChain
# from langchain_openai import ChatOpenAI  # Replace with your GPT-4o-mini integration if needed
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the LLM (choose GPT-4o or Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")  # Or use ChatOpenAI(model="gpt-4o-mini")

# Prompt Template for Resume Tailoring
prompt_template = """
Role: You are a professional resume tailoring expert specializing in optimizing resumes for job applications.

Problem Statement: Many candidates’ resumes do not effectively highlight the achievements, responsibilities, and skills most relevant to the job. Your task is to modify the provided resume sections to align better with the job description while maintaining factual accuracy.

Job Description:
{job_description}

Input Resume Sections:
{input_json}

Instructions:
1. Modify "work_experience":
   - Reorder and refine bullet points to emphasize relevant accomplishments.
   - Rephrase bullet points to integrate key job requirements while keeping factual accuracy.
2. Modify "skills":
   - Prioritize skills most relevant to the job description.
   - Optionally, enhance the formatting to better reflect proficiency.
3. Output the modified sections in JSON format:
{{
  "modified_work_experience": [ ... ],
  "modified_skills": [ ... ]
}}
Do not include any extra text—only output the final JSON.
"""

# Create a LangChain prompt template
prompt = PromptTemplate(input_variables=["job_description", "input_json"], template=prompt_template)

# Create an LLMChain
chain = LLMChain(llm=llm, prompt=prompt)


def tailor_resume_for_job(user_info, job_description):
    """
    Enhances user_info to align with a specific job_description using LLM.
    """
    input_json_str = json.dumps(user_info, indent=2)
    result = chain.run(job_description=job_description, input_json=input_json_str)
    structured_result = re.sub(r"^```(?:json)?\s*|\s*```$", "", result)

    try:
        return json.loads(structured_result)  # Convert string JSON response to Python dictionary
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON from LLM response.")
        return None


def extract_relevant_user_info(user_info):
    """
    Extracts only relevant fields (work experience, skills, position, company) from user_info.
    """
    extracted_info = {
        "current_position": user_info.get("Current Position", ""),
        "current_company": user_info.get("Current Company", ""),
        "work_experience": user_info.get("Work Experience", []),
        "skills": user_info.get("Technical Skills", [])
    }
    return extracted_info


def extract_relevant_job_data(job_data_list):
    """
    Extracts only relevant fields (title, company, job_description) from job_data_list.
    """
    return [
        {
            "title": job["title"],
            "company": job["company"],
            "job_description": job["job_description"]
        }
        for job in job_data_list
    ]


def optimize_resume_for_jobs(user_info, job_data_list):
    """
    Processes user_info for multiple job descriptions.
    """
    extracted_user_info = extract_relevant_user_info(user_info)
    relevant_jobs = extract_relevant_job_data(job_data_list)
    tailored_results = []

    for i, job_data in enumerate(relevant_jobs[:5]):  # Limit to 5 jobs
        print(f"Processing Job {i + 1}: {job_data['title']} at {job_data['company']}")
        modified_resume = tailor_resume_for_job(extracted_user_info, job_data["job_description"])

        if modified_resume:
            tailored_results.append({
                "job_title": job_data["title"],
                "company": job_data["company"],
                "modified_resume": modified_resume
            })

    return tailored_results


# if __name__ == "__main__":
#     # Sample Input
#     user_info = {
#         "work_experience": [
#             {"company": "Company A", "role": "Software Engineer",
#              "responsibilities": ["Developed APIs", "Managed cloud deployments"]}
#         ],
#         "skills": ["Python", "SQL", "Machine Learning"]
#     }
#
#     job_data_list = [
#         {"title": "Data Scientist", "company": "Google",
#          "job_description": "Looking for a data scientist skilled in Python and SQL."},
#         {"title": "ML Engineer", "company": "Amazon",
#          "job_description": "Machine learning engineer needed with cloud experience."},
#         {"title": "AI Researcher", "company": "Meta", "job_description": "AI researcher required with NLP expertise."},
#         {"title": "Software Engineer", "company": "Microsoft",
#          "job_description": "Backend developer skilled in APIs and cloud."},
#         {"title": "Cloud Architect", "company": "IBM",
#          "job_description": "Looking for a cloud architect with Kubernetes experience."}
#     ]
#
#     # Process user_info for multiple jobs
#     final_results = process_all_jobs(user_info, job_data_list)
#
#     # Print formatted results
#     print(json.dumps(final_results, indent=2))
