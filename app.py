import streamlit as st
import time
from config import GROQ_API_KEY, PAGE_CONFIG
from ui_components import set_custom_css, display_title, upload_ui, job_desc_ui, results_placeholder_ui, interview_prep_ui
from utils import extract_pdf_text, calculate_similarity_bert, extract_scores
from ai_service import generate_report, generate_interview_advice
 
# Set page configuration
st.set_page_config(**PAGE_CONFIG)
 
# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "input"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_filename" not in st.session_state:
    st.session_state.resume_filename = ""
if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""
if "report" not in st.session_state:
    st.session_state.report = ""
if "ats_score" not in st.session_state:
    st.session_state.ats_score = None
if "avg_score_pct" not in st.session_state:
    st.session_state.avg_score_pct = None
if "interview_advice" not in st.session_state:
    st.session_state.interview_advice = ""
 
# Set up UI components
set_custom_css()
display_title()
 
tabs = st.tabs(["1️⃣ Upload", "2️⃣ Job Description", "3️⃣ Results", "4️⃣ Interview Prep"])
 
with tabs[0]:
    uploaded_file = upload_ui()
 
with tabs[1]:
    job_desc_ui()
 
with tabs[2]:
    results_placeholder_ui()
 
with tabs[3]:
    interview_prep_ui()
 
# Processing logic
if st.session_state.step == "processing":
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        prog = st.progress(0)
        status = st.text("Step 1/3 — Extracting resume text")
        try:
            uploaded_file.seek(0)
        except Exception:
            pass
        with st.spinner("Extracting text from resume..."):
            resume_text = extract_pdf_text(uploaded_file)
            time.sleep(0.4)
        prog.progress(33)
        status.text("Step 2/3 — Calculating similarity score")
        with st.spinner("Calculating similarity against job description..."):
            ats = calculate_similarity_bert(resume_text or " ", st.session_state.job_desc or " ")
            time.sleep(0.4)
        prog.progress(66)
        status.text("Step 3/3 — Generating AI report")
        with st.spinner("Calling LLM to generate detailed analysis. This can take a while..."):
            report_text = generate_report(resume_text, st.session_state.job_desc)
            time.sleep(0.6)
        prog.progress(100)
        st.markdown('</div>', unsafe_allow_html=True)
        st.success("Analysis complete")
    st.session_state.resume_text = resume_text
    st.session_state.ats_score = ats
    st.session_state.report = report_text
    scores = extract_scores(report_text)
    if scores:
      avg_pct = (sum(scores) / (5 * len(scores))) * 100
        st.session_state.avg_score_pct = avg_pct
    else:
        st.session_state.avg_score_pct = None
    st.session_state.step = "results"
    st.rerun()
 
# Results display
if st.session_state.step == "results":
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(f"### Analysis for: **{st.session_state.resume_filename}**")
        st.markdown(f"**Job Description snippet:** {st.session_state.job_desc[:180]}...")
    with header_col2:
        if st.session_state.avg_score_pct is not None:
            st.metric(label="Overall AI Fit", value=f"{st.session_state.avg_score_pct:.1f}%", delta=None)
        else:
            st.metric(label="Overall AI Fit", value="N/A", delta=None)
 
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.session_state.ats_score is not None:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**Similarity Score (ATS-like)**")
            st.markdown(f"<div class='score-large'>{st.session_state.ats_score:.3f}</div>", unsafe_allow_html=True)
            st.markdown("<div class='muted'>Higher means the resume text is closer to the JD.</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Similarity score could not be calculated.")
    with col2:
        if st.session_state.avg_score_pct is not None:
            color = "#0b7a4a" if st.session_state.avg_score_pct >= 70 else ("#ffc107" if st.session_state.avg_score_pct >= 40 else "#d32f2f")
            st.markdown(f"""
            <div style="background:#f7fff8;border-radius:10px;padding:14px;border:1px solid #e6f4ea;text-align:center;">
              <div style="font-size:14px;font-weight:600;">AI Average Score</div>
              <div style="font-size:34px;font-weight:700;color:{color};">{st.session_state.avg_score_pct:.1f}%</div>
              <div style="color:#6b7280;">Based on detailed LLM evaluation</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("AI report did not include numeric scores.")
 
    st.divider()
    with st.expander("🔍 View Full AI Generated Analysis Report", expanded=True):
        st.markdown(
            f"""<div style="background:#fbfbfd;padding:16px;border-radius:10px;border:1px solid #eceff6;max-height:520px;overflow:auto;white-space:pre-wrap;">{st.session_state.report}</div>""",
            unsafe_allow_html=True,
        )
 
    dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 1])
    with dl_col2:
        st.download_button(
            label="📥 Download Full Report",
            data=st.session_state.report,
            file_name="ai_resume_analysis.txt",
            use_container_width=True,
        )
 
    st.divider()
    action_cols = st.columns([1, 1, 1])
    if action_cols[0].button("🔁 Re-run Analysis"):
        st.session_state.step = "processing"
        st.rerun()
 
    if action_cols[1].button("📝 Edit Job Description"):
        st.session_state.step = "job"
        st.rerun()
 
    if action_cols[2].button("📄 Upload New Resume"):
        st.session_state.step = "input"
        st.rerun()
      
