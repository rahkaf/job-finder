import asyncio
import uuid
import sys
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

import os
from google import genai
from app.tools import read_resume, search_jobs, send_email_report

load_dotenv()

def main():
    print("Running job finder pipeline...", flush=True)
    
    # 1. Read resume
    print("Reading resume...", flush=True)
    resume_text = read_resume("Fakhar_Zikri_Resume_FullTime_AIEngineering.pdf")
    
    # 2. Search jobs
    print("Searching jobs...", flush=True)
    jobs_text = search_jobs("AI Engineer remote jobs", max_results=10)
    
    # 3. Use Gemini to score and write email
    print("Generating report...", flush=True)
    import time
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = f"""You are an AI job finder. Review the following resume and job listings. 
Score each job (0-100) based on how well it matches the resume. 
Write a well-formatted email report of the best matches.

Resume: {resume_text[:2000]}...

Jobs: {jobs_text}
"""
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            report = response.text
            break
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"Rate limited. Waiting 20 seconds...", flush=True)
                time.sleep(20)
            else:
                raise e
    
    # 4. Send email
    print("Sending email...", flush=True)
    send_email_report("Daily Job Report - AI Engineering", report)
    print("Done!", flush=True)

if __name__ == "__main__":
    main()
