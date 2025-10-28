from groq import Groq
from config import GROQ_API_KEY
from prompts import REPORT_PROMPT, INTERVIEW_PROMPT
 
def generate_report(resume, job_desc):
    if not GROQ_API_KEY:
        return "Error: LLM API key not configured. Set GROQ_API_KEY in your environment."
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = REPORT_PROMPT.format(resume=resume, job_desc=job_desc)
        resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error generating report: {str(e)}"
 
def generate_interview_advice(resume_text, job_desc):
    if not GROQ_API_KEY:
        return "Error: LLM API key not configured. Set GROQ_API_KEY in your environment."
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = INTERVIEW_PROMPT.format(resume_text=resume_text, job_desc=job_desc)
        resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error generating interview prep: {str(e)}"
