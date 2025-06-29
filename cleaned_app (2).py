
import streamlit as st
import pdfplumber
import docx
import re
import textstat
import time

st.title("Resume ATS Matcher")

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else "Not found"

def get_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

def analyze_soft_signals(text):
    signals = {}
    leadership_words = ["led", "managed", "initiated", "coordinated", "supervised", "mentored"]
    action_verbs = ["developed", "designed", "created", "implemented", "built", "executed"]
    signals['Leadership Signals'] = sum(text.lower().count(word) for word in leadership_words)
    signals['Action Verbs'] = sum(text.lower().count(word) for word in action_verbs)
    signals['Readability Score'] = round(textstat.flesch_reading_ease(text), 2)
    signals['Average Sentence Length'] = round(textstat.avg_sentence_length(text), 2)
    return signals

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"], key="resume_upload")

if uploaded_file:
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")
    resume_text = ""
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(uploaded_file)

    st.subheader("Parsed Resume Data")
    st.write("📧 Email:", extract_email(resume_text))
    st.text_area("📝 Full Resume Text", resume_text[:3000])

    job_description = """
    We are looking for a Python developer with experience in data analysis, Pandas, NumPy, and machine learning.
    Strong problem-solving skills and knowledge of Flask or Django is a plus.
    """
    st.subheader("🔍 ATS Match Score")
    jd_keywords = get_keywords(job_description)
    resume_keywords = get_keywords(resume_text)
    matched = jd_keywords & resume_keywords
    match_score = round(len(matched) / len(jd_keywords) * 100)
    st.write("✅ Matched Keywords:", ", ".join(matched))
    st.write("🎯 Match Score:", f"{match_score}%")
    if match_score >= 70:
        st.success("Great match! You're a strong fit for this job.")
    elif match_score >= 40:
        st.warning("Decent match. Consider tailoring your resume more.")
    else:
        st.error("Low match. Resume needs improvement.")

    st.subheader("🧠 Soft Signal Analysis")
    soft_signals = analyze_soft_signals(resume_text)
    for k, v in soft_signals.items():
        st.write(f"{k}: {v}")
    if soft_signals['Leadership Signals'] >= 3:
        st.success("Strong leadership tone.")
    else:
        st.warning("Add more leadership-oriented language.")
    if soft_signals['Action Verbs'] >= 4:
        st.success("Good use of action verbs.")
    else:
        st.warning("Consider using more impactful action verbs.")

    st.subheader("🏢 Company HR Style Registration")
    with st.form("hr_form"):
        company_name = st.text_input("Company Name")
        location = st.text_input("Location")
        core_domain = st.text_input("Company Core Area (e.g., AI, Finance, Software)")
        qualifications = st.text_area("Required Qualifications")
        hiring_style = st.selectbox("Hiring Style", ["Google-style", "Startup-style", "Amazon-style", "Custom"])
        interview_type = st.selectbox("Interview Type", ["Technical", "Behavioral", "Both"])
        hr_logic = st.text_area("Define HR Interview Style / Questions")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Company profile registered successfully!")
            st.session_state["registered_company"] = {
                "name": company_name,
                "location": location,
                "domain": core_domain,
                "qualifications": qualifications,
                "style": hiring_style,
                "interview_type": interview_type,
                "hr_logic": hr_logic
            }

    st.subheader("🤖 HR Chat Simulation")
    hr_questions = [
        "Tell me about yourself.",
        "Why do you want to join our company?",
        "Describe a challenge you faced and how you handled it.",
        "Where do you see yourself in 5 years?"
    ]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for i, q in enumerate(hr_questions):
        st.write(f"**Q{i+1}: {q}**")
        user_input = st.text_input(f"Your Answer {i+1}", key=f"answer_{i}")
        if user_input == "":
            time.sleep(5)
            sample_answer = "Sample Answer: I am a self-motivated individual who enjoys working on innovative projects."
            st.info(sample_answer)
        else:
            st.success("Answer submitted.")
        st.session_state.chat_history.append((q, user_input or sample_answer))
