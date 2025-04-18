from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize LLM Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# Define the prompt template
job_ranking_template = """
User Information:
Experience: {experience} years
Current Position: {current_position}
Current Company: {current_company}
Technical Skills: {technical_skills}
Brief Summary: {brief_summary}

Job Descriptions:
{job_descriptions}

Please rank the jobs from most to least suitable based on relevance to the user's experience, position, and skills. 
Only return the job indices in descending order, separated by commas.
"""

# Define the prompt
prompt = PromptTemplate(
    input_variables=["experience", "current_position", "current_company", "technical_skills", "brief_summary", "job_descriptions"],
    template=job_ranking_template
)


# def format_job_descriptions(job_listings):
#     """
#     Formats the job descriptions for the prompt.
#     """
#     return "\n".join(
#         [f"{i + 1}. {job['title']} at {job['companyName']}: {job.get('description', 'No description available')}"
#          for i, job in enumerate(job_listings)]
#     )

def format_job_descriptions(job_listings):
    """
    Formats the job descriptions for the prompt.
    """
    return "\n".join(
        [
            f"{i + 1}. {job['title']} at {job['company']}:\n"
            f"   {job.get('job_description', 'No description available')}\n"
            for i, job in enumerate(job_listings)
        ]
    )

def rank_jobs_with_gemini(user_info, job_listings):
    """
    Ranks job listings using Gemini LLM with LangChain.

    Args:
        user_info (dict): Extracted user information (skills, experience, current position, etc.).
        job_listings (list): List of job dictionaries with descriptions.

    Returns:
        list: Top 5 ranked job listings.
    """
    # Prepare job descriptions
    job_descriptions = format_job_descriptions(job_listings)

    # Prepare the prompt inputs
    prompt_text = prompt.format(
        experience=user_info.get('Experience', 'N/A'),
        current_position=user_info.get('Current Position', 'N/A'),
        current_company=user_info.get('Current Company', 'N/A'),
        technical_skills=", ".join(user_info.get('Technical Skills', [])),
        brief_summary=user_info.get('Brief Summary', 'N/A'),
        job_descriptions=job_descriptions
    )

    # Query the Gemini LLM
    response = llm.invoke(prompt_text)
    response_text = response.content  # Extracting response content

    # Parse the response to get job indices
    ranked_indices = [int(idx.strip()) - 1 for idx in response_text.split(',') if idx.strip().isdigit()]

    # Return the top 5 job listings
    top_5_jobs = [job_listings[i] for i in ranked_indices[:5] if 0 <= i < len(job_listings)]

    return top_5_jobs


# Example usage
if __name__ == "__main__":
    # Mock user info and job listings for testing
    user_info = {
        "experience": 5,
        "current_position": "Data Scientist",
        "current_company": "TechCorp",
        "technical_skills": ["Python", "Machine Learning", "Data Analysis"],
        "brief_summary": "A results-driven data scientist with expertise in predictive modeling."
    }

    job_listings = [
        {"title": "Senior Data Scientist", "company": "InnovateAI", "description": "Leading predictive modeling projects."},
        {"title": "ML Engineer", "company": "NextGenTech", "description": "Developing scalable machine learning models."},
        {"title": "Data Analyst", "company": "DataSolutions", "description": "Analyzing data trends and generating insights."},
    ]

    ranked_jobs = rank_jobs_with_gemini(user_info, job_listings)
    print("Top 5 Recommended Jobs:", ranked_jobs)