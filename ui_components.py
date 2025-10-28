import streamlit as st
from ai_service import generate_interview_advice
 
def set_custom_css():
    st.markdown(
        """
        <style>
        .title {font-size:28px; font-weight:700; color:#0B3D91; margin-bottom:6px;}
        .subtitle {color:#444444; margin-top:0; margin-bottom:18px;}
        .card {background:#ffffff;border:1px solid #e6e9ef;padding:14px;border-radius:10px;}
        .score-large {font-size:34px; font-weight:700;}
        .muted {color:#6b7280;}
        </style>
        """,
        unsafe_allow_html=True,
    )
 
def display_title():
    st.markdown('<div class="title">🧠 AI Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload your resume and paste the job description to get a similarity score and an AI analysis report.</div>', unsafe_allow_html=True)
 
def upload_ui():
    with st.container():
        c1, c2 = st.columns([2, 1])
        with c1:
            uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"], key="uploader")
            if uploaded_file:
                st.session_state.resume_filename = uploaded_file.name
                try:
                    preview_text = extract_text(uploaded_file, maxpages=1)
                except Exception:
                    uploaded_file.seek(0)
                    try:
                        preview_text = extract_text(uploaded_file)
                    except Exception:
                        preview_text = ""
                if preview_text:
                    with st.expander("Preview extracted text (first 300 chars)"):
                        st.write(preview_text[:300])
        with c2:
            st.markdown("**Need help?**")
            st.markdown("- Use a clean, text-based PDF\n- Avoid scanned images without OCR\n")
    st.divider()
    col_action = st.columns([1, 1])
    if col_action[1].button("Next: Job Description", use_container_width=True):
        st.session_state.step = "job"
        st.session_state.job_desc = st.session_state.get("job_desc", "")
        st.rerun()
    return uploaded_file
 
def job_desc_ui():
    with st.container():
        jd_text = st.text_area("💼 Paste Job Description", placeholder="Enter the job description here...", height=240, key="jd")
        if jd_text:
            st.session_state.job_desc = jd_text
    st.divider()
    col_back_next = st.columns([1, 1])
    if col_back_next[0].button("← Back to Upload", use_container_width=True):
        st.session_state.step = "input"
        st.rerun()
 
    if col_back_next[1].button("Analyze ▶️", use_container_width=True):
        if not st.session_state.resume_filename and not st.session_state.job_desc:
