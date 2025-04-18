import json


def generate_final_api_response(user_info, job_data, optimized_user_info):
    """
    Generates a final API response JSON structure by combining the user info,
    job postings, and the optimized resume details for each job.
    """
    # Extract and organize personal details from the resume data
    personal_details = {
        "full_name": user_info.get("Full Name"),
        "email": user_info.get("Email Address"),
        "phone_number": user_info.get("Phone Number"),
        "physical_address": user_info.get("Physical Address"),
        "linkedin": user_info.get("LinkedIn URL"),
        "personal_website": user_info.get("Personal Website or Portfolio URL"),
        "github": user_info.get("Github URL"),
        "brief_summary": user_info.get("Brief Summary"),
        "experience_years": user_info.get("Experience"),
        "education": user_info.get("Education"),
        # "technical_skills": user_info.get("Technical Skills"),
        "languages": user_info.get("Languages"),
        "current_position": user_info.get("Current Position"),
        "current_company": user_info.get("Current Company"),
        # "work_experience": user_info.get("Work Experience")
    }

    # Create a list to store job opportunities with the customized resume details
    job_opportunities = []
    for job in job_data:
        job_entry = {
            "job_title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "place": job.get("place"),
            "job_url": job.get("job_url"),
            "apply_link": job.get("apply_link"),
            "posted_date": job.get("date"),
            "job_description": job.get("job_description"),
            "job_id": job.get("job_id")
        }

        # Try to find a matching optimized resume based on job title and company
        customized_resume = {}
        for optimized in optimized_user_info:
            if optimized.get("job_title") == job.get("title") and optimized.get("company") == job.get("company"):
                customized_resume = optimized.get("modified_resume", {})
                break
        job_entry["customized_resume"] = customized_resume

        job_opportunities.append(job_entry)

    # Combine everything into one final response structure
    final_response = {
        "personal_details": personal_details,
        "job_opportunities": job_opportunities
    }

    return final_response


# if __name__ == "__main__":
#     # Example input data (replace with your actual data as needed)
#     user_info = {
#         'Full Name': 'Yash Rajput',
#         'Email Address': 'yashrajput.0305@gmail.com',
#         'Phone Number': '+91-7223021688',
#         'Physical Address': '462 Shyam Nagar, Indore',
#         'LinkedIn URL': 'linkedin.com/in/yash-rajput-198345226',
#         'Personal Website or Portfolio URL': 'None',
#         'Github URL': 'None',
#         'Experience': '1',
#         'Brief Summary': 'AI/ML Developer with 1 year of experience, specializing in building AI agents and Generative AI solutions. Proficient in developing RAG-based applications and leveraging machine learning for data-driven decision-making. Passionate about creating innovative AI systems to drive impactful results.',
#         'Education': 'Medicaps University\nBachelor of Technology, Computer Science\nJune 2024\nRelated Coursework: Computer Science, Machine Learning, Generative AI\nCGPA: 8.84',
#         'Technical Skills': ['Python', 'Langchain', 'Langgraph', 'OpenAI API', 'LlamaIndex', 'CrewAI', 'Hugging Face',
#                              'Matplotlib', 'Seaborn', 'Git', 'GitHub', 'NumPy', 'Pandas', 'Scikit-learn'],
#         'Languages': ['English', 'Hindi'],
#         'Current Position': 'AI/ML Developer',
#         'Current Company': 'Ksolves India ltd.',
#         'Work Experience': [{
#             'Job Title': 'AI/ML Developer',
#             'Company': 'Ksolves India ltd.',
#             'Responsibilities': [
#                 'Developed a Multi-Agent System Using LangGraph',
#                 'Created a Retrieval-Augmented Generation (RAG) Application',
#                 'Explored Conversational AI with Dialogflow',
#                 'Built a Clustering Solution with DBSCAN',
#                 'Conducted RAG Evaluation'
#             ]
#         }]
#     }
#
#     job_data = [
#         {
#             'title': 'AI/ML Engineer',
#             'company': 'Onix',
#             'location': 'India',
#             'place': 'Pune, Maharashtra, India',
#             'job_url': 'https://in.linkedin.com/jobs/view/ai-ml-engineer-at-onix-4191423516?position=1&pageNum=0&refId=xQ8QcQRDh8Tlng10ni8bHg%3D%3D&trackingId=3ab9RN59IlYZ0SdCOGKmFQ%3D%3D',
#             'apply_link': '',
#             'date': '2025-03-26',
#             'job_description': "Title: AI/ML Engineer\n\nJob location: Pune\n\nTeam: Product Engineering\n\n ",
#             'job_id': '4191423516'
#         }
#     ]
#
#     optimized_user_info = [
#         {
#             'job_title': 'AI/ML Engineer',
#             'company': 'Onix',
#             'modified_resume': {
#                 'modified_work_experience': [{
#                     'Job Title': 'AI/ML Developer',
#                     'Company': 'Ksolves India ltd.',
#                     'Responsibilities': [
#                         'Developed and deployed a Retrieval-Augmented Generation (RAG) system, integrating knowledge retrieval with generative models for context-aware responses.',
#                         'Designed and implemented a scalable multi-agent architecture using LangGraph to optimize task automation.',
#                         'Utilized Langchain, LlamaIndex, and OpenAI API to build and optimize AI/ML models.',
#                         'Developed a clustering solution using DBSCAN to identify meaningful data patterns.',
#                         'Created evaluation frameworks for RAG applications, ensuring performance and relevance.',
#                         'Developed a conversational AI POC using Dialogflow.'
#                     ]
#                 }],
#                 'modified_skills': ['Python', 'Langchain', 'Langgraph', 'LlamaIndex', 'Hugging Face', 'OpenAI API',
#                                     'Scikit-learn', 'NumPy', 'Pandas', 'Git', 'GitHub', 'Matplotlib', 'Seaborn',
#                                     'CrewAI']
#             }
#         }
#     ]
#
#     # Generate the final API response JSON structure
#     final_response = generate_final_api_response(user_info, job_data, optimized_user_info)
#
#     # Print the output in a nicely formatted JSON string
#     print(json.dumps(final_response, indent=4))
