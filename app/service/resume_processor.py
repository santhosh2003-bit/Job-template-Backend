import fitz  # PyMuPDF for extracting text from PDFs
import re
import json
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize LLM Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")


def extract_text_from_pdf(pdf_path):
    """
    Extracts text content from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted plain text from the PDF.
    """
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def generate_system_prompt():
    """
    Generates the system prompt for structured resume information extraction.

    Returns:
        str: System prompt string.
    """
    current_year = datetime.now().year

    # return f"""You are a resume information extraction expert. Your task is to analyze a block of plain text (which is the parsed content of a resume) and extract the following fields with the rules specified below. Your output must be in a structured JSON format with each field as a key. If any field is not found, output "None" for that field.
    #
    # Extract the following fields:
    # - "Full Name": The candidate's complete name.
    # - "Email Address": A valid email address.
    # - "Phone Number": The candidate's primary phone number.
    # - "Physical Address": The candidate's mailing or residential address.
    # - "LinkedIn URL": A URL linking to the candidate’s LinkedIn profile.
    # - "Personal Website or Portfolio URL": A URL for the candidate’s personal website or portfolio.
    # - "Github URL": A URL linking to the candidate’s Github profile.
    # - "Experience": Total years or description of work experience, but do NOT count any internships as experience. Only include full-time or permanent roles (current year: {current_year}).
    # - "Brief Summary": A concise professional summary or objective statement.
    # - "Education": Details about degrees, institutions, graduation dates, etc.
    # - "Technical Skills": A python list of technical skills or technologies mentioned.
    # - "Languages": A python list of languages the candidate is proficient in (this may include spoken languages and/or programming languages, as applicable).
    # - "Current Position": The candidate’s current job title.
    # - "Current Company": The name of the candidate’s current employer.
    #
    # Additional instructions:
    # 1. Do not extract internship experiences in the "Experience" field; if the text only contains internships, set "Experience" to 0.
    # 2. Use context clues to ensure accuracy, and choose the most relevant or likely information if multiple options are present.
    # 3. Clean and normalize the extracted data (for example, trim extra whitespace, ensure URLs are complete, etc.).
    # 4. Return the output in strict JSON format with the keys exactly as specified above.
    # 5. Do not include any commentary or additional text beyond the JSON object.
    #
    # When you are done, output only the JSON object with the keys and their respective values."""

    return f"""You are a resume information extraction expert. Your task is to analyze a block of plain text (which is the parsed content of a resume) and extract the following fields with the rules specified below. Your output must be in a structured JSON format with each field as a key. If any field is not found, output "None" for that field.

            Extract the following fields:
            - "Full Name": The candidate's complete name.
            - "Email Address": A valid email address.
            - "Phone Number": The candidate's primary phone number.
            - "Physical Address": The candidate's mailing or residential address.
            - "LinkedIn URL": A URL linking to the candidate’s LinkedIn profile.
            - "Personal Website or Portfolio URL": A URL for the candidate’s personal website or portfolio.
            - "Github URL": A URL linking to the candidate’s Github profile.
            - "Experience": Total years or description of work experience, but do NOT count any internships as experience. Only include full-time or permanent roles (current year: {current_year}).
            - "Brief Summary": A concise professional summary or objective statement.
            - "Education": Details about degrees, institutions, graduation dates, etc.
            - "Technical Skills": A python list of technical skills or technologies mentioned.
            - "Languages": A python list of languages the candidate is proficient in (this may include spoken languages and/or programming languages, as applicable).
            - "Current Position": The candidate’s current job title.
            - "Current Company": The name of the candidate’s current employer.
            - "Work Experience": A detailed breakdown of past work experience in the following structured format:
                ```json
                    "work_experience": [
                        {{
                            "Job Title": "Senior Data Scientist",
                            "Company": "Resume Worded",
                            "Responsibilities": [
                                "Led a cross-functional team of 10 in implementing machine learning models, increasing efficiency of predictive analysis by 20%",
                                "Managed data pipeline using PySpark and Python, refining data processing time by 18%",
                                "Developed and optimized probabilistic models, improving predictive accuracy by 15%",
                                "Designed an automatic report-distribution system using SQL and Shiny, saving approximately 10 hours weekly",
                                "Facilitated company-wide data science training, enhancing overall analytical skills by 20%"
                            ]
                        }},
                        {{
                            "Job Title": "Data Scientist",
                            "Company": "IBM",
                            "Responsibilities": [
                                "Created scalable machine learning algorithms, automating manual processes and increasing team productivity by 30%",
                                "Used Elastic Map Reduce (EMR) to handle large datasets, reducing processing time by 25%"
                            ]
                        }}
                    ]
                ```
            
            Additional instructions:
            1. Do not extract internship experiences in the "Experience" field; if the text only contains internships, set "Experience" to 0.
            2. Ensure that each job in "Work Experience" contains a "Job Title", "Company", and a list of key responsibilities.
            3. Use context clues to ensure accuracy, and choose the most relevant or likely information if multiple options are present.
            4. Clean and normalize the extracted data (for example, trim extra whitespace, ensure URLs are complete, etc.).
            5. Return the output in strict JSON format with the keys exactly as specified above.
            6. Do not include any commentary or additional text beyond the JSON object.
            
            When you are done, output only the JSON object with the keys and their respective values."""



def extract_resume_data(pdf_text):
    """
    Extracts structured information from a resume text using LLM.

    Args:
        pdf_text (str): Extracted text from the resume PDF.

    Returns:
        dict: Parsed structured resume data.
    """
    messages = [
        ("system", generate_system_prompt()),
        ("user", pdf_text)
    ]

    # try:
    response = llm.invoke(messages)
    structured_resume_data = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.content)
    return json.loads(structured_resume_data)
    # except Exception as e:
    #     print(f"Error processing resume data: {e}")
    #     return {"error": "Failed to process resume data"}


def process_resume(pdf_path):
    """
    Complete pipeline to process a resume:
    1. Extract text from the PDF.
    2. Extract structured resume data using LLM.

    Args:
        pdf_path (str): Path to the resume PDF.

    Returns:
        dict: Extracted resume information.
    """
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        return {"error": "No text extracted from the PDF"}

    return extract_resume_data(raw_text)
