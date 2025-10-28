import os
from dotenv import load_dotenv
 
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
 
PAGE_CONFIG = {
    "page_title": "AI Resume Analyzer",
    "layout": "centered"
}
