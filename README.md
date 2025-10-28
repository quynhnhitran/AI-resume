# 🧠 AI Resume Analyzer

An application built with **Streamlit** and powered by the **Groq API** and a **BERT** Sentence Transformer model to provide comprehensive, instant analysis of a candidate's resume against a specific job description.

This tool aims to simulate an **ATS (Applicant Tracking System)** evaluation while leveraging the power of **Large Language Models (LLMs)** for deep, contextualized feedback and interview preparation.

## 🧠 Demo Steps:

Our application provides a professional resume analysis process in just a few simple steps:

### 1. Upload Your Resume

Start by uploading your resume PDF file. The intuitive interface will guide you.
![Step 1: Upload Resume](https://github.com/user-attachments/assets/842ea394-55ca-4195-a8ee-951b84a7f0b4)

### 2. Input Job Description

Paste the desired job description so the AI can assess the match level.
<br>
| <img width="600" height="365" alt="image" src="https://github.com/user-attachments/assets/2547e6e2-e0e4-4d1c-ba31-2c3f46846271" /> |
| :--- |
![Step 2: Enter Job Description](https://github.com/user-attachments/assets/3b259244-3970-46e7-9901-db6d71e1e944)
---

### 3. View AI Analysis Report & Interview Prep

Instantly receive a detailed AI report and helpful advice to prepare for the interview.

<br>

| AI Analysis Report | Interview Preparation |
| :--- | :--- |
| ![AI Analysis Report](https://github.com/user-attachments/assets/44a1d30c-0bf5-464e-9be3-e77d160ad981) | ![Interview Preparation](https://github.com/user-attachments/assets/18b476ec-1861-48ae-b1f1-8e4dc09042dc) |
---

## 🛠️ Key Features and Technical Highlights

This project demonstrates proficiency in several key technical domains:

### 1. Advanced LLM Integration & Prompt Engineering
* **Groq API Utilization:** Leverages the **Groq LPU Inference Engine** via the `groq-sdk` for blazing-fast, low-latency generation of detailed reports and interview advice.
    * **Model:** Utilizes the high-performance `llama-3.3-70b-versatile` model for high-quality, nuanced analysis.
* **Contextual Prompting:** Implements dedicated, complex **system prompts** (`REPORT_PROMPT`, `INTERVIEW_PROMPT`) to direct the LLM's output for specific tasks:
    * Generating a structured **Resume Analysis Report** with granular scores (e.g., `3/5`).
    * Creating targeted **Interview Questions** and identifying **Skills Gaps**.
* **Decoupled AI Service:** The core AI logic is encapsulated in `ai_service.py`, ensuring a clean separation of concerns and making the LLM calls easily maintainable and switchable.

### 2. Semantic Similarity and Natural Language Processing (NLP)
* **ATS Score Simulation:** Implements a text similarity score to mimic an ATS-like evaluation.
* **State-of-the-Art Embedding:** Uses the **`sentence-transformers/all-mpnet-base-v2` (BERT-based)** model to generate high-quality vector embeddings for the resume and job description.
* **Cosine Similarity:** Calculates the **Cosine Similarity** between the resume and JD embeddings to provide a quantitative "match score." This is a robust measure of semantic closeness, demonstrating knowledge of modern NLP techniques.

### 3. Interactive Web Application Development (Streamlit)
* **Full-Stack Prototyping:** Built the complete interactive frontend and backend logic using **Streamlit**, enabling rapid deployment of a data-intensive web application.
* **State Management:** Effectively manages the application workflow across multiple steps (`input`, `job`, `processing`, `results`) using **`st.session_state`** for a seamless, multi-page user experience (achieved via tabs and explicit state transitions with `st.rerun()`).
* **Robust UI/UX:** Features custom CSS for a professional look (`ui_components.py`), a multi-step progress bar, clear status messages, and dedicated sections for file upload, job description input, analysis results, and interview prep.
* **Dynamic Data Extraction:** Implements utility functions (`utils.py`) for reliable **PDF Text Extraction** using `pdfminer.six` and uses **RegEx** (`re` module) to parse numeric scores from the unstructured LLM output.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

* Python 3.8+
* A Groq API Key

### Installation

1.  **Clone the repository (or set up the files):**
    ```bash
    # Assuming you have the files in a project directory
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    # On Windows
    ./venv/Scripts/activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    Create a file named **`.env`** in the root directory and add your Groq API key:
    ```
    # .env
    GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
    ```

### Running the Application

1.  **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2.  **Access:** The application will open automatically in your browser (usually at `http://localhost:8501`).

---

## 📁 Project Structure

| File | Description |
| :--- | :--- |
| `app.py` | **Main application entry point.** Handles Streamlit UI flow, session state, processing logic, and result display. |
| `ai_service.py` | **LLM Service Layer.** Contains functions (`generate_report`, `generate_interview_advice`) for interacting with the Groq API. |
| `utils.py` | **Utility Functions.** Handles PDF text extraction (`pdfminer.six`), BERT-based similarity calculation (`sentence-transformers`, `scikit-learn`), and score extraction (RegEx). |
| `ui_components.py` | **Streamlit UI Components.** Defines reusable functions for UI elements (CSS, headers, input fields, and the Interview Prep tab logic). |
| `prompts.py` | **Prompt Templates.** Stores the structured text templates used to guide the Groq LLM for specific analysis tasks. |
| `config.py` | **Configuration.** Loads environment variables (e.g., `GROQ_API_KEY`) and sets Streamlit page configuration. |
| `requirements.txt` | **Dependencies.** Lists all required Python packages (e.g., `streamlit`, `groq`, `sentence-transformers`). |
