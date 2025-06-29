
import streamlit as st
import fitz  # PyMuPDF
import docx2txt
import re
import spacy
import tempfile
import json

st.title("📄 AI Resume Sculptor")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"], key="resume_upload")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        filename = tmp_file.name

    def extract_text(filename):
        if filename.endswith(".pdf"):
            doc = fitz.open(filename)
            text = ""
            for page in doc:
                text += page.get_text("text")
            return text
        elif filename.endswith(".docx"):
            return docx2txt.process(filename)
        return ""

    def extract_contact(text):
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)
        phone = re.findall(r"\+?\d[\d\s\-]{8,}", text)
        return email[0] if email else "", phone[0] if phone else ""

    def extract_name(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Name Not Found"

    def extract_skills(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text.lower())
        common_skills = ['python', 'java', 'sql', 'machine learning', 'data analysis', 'communication', 'leadership']
        skills = [token.text for token in doc if token.text in common_skills]
        return list(set(skills))

    text = extract_text(filename)
    name = extract_name(text)
    email, phone = extract_contact(text)
    skills = extract_skills(text)

    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills
    }

    st.subheader("📋 Extracted Resume Data")
    st.write("**Name:**", name)
    st.write("**Email:**", email)
    st.write("**Phone:**", phone)
    st.write("**Skills:**", ", ".join(skills))
    st.text_area("📝 Full Resume Text", text[:3000])
    st.subheader("📦 JSON Output")
    st.json(resume_data)

    company_profile = {
        "company": "Amazon",
        "hiring_style": "Fast-paced, leadership-focused, deep tech",
        "required_skills": ["python", "java", "leadership", "machine learning", "communication"],
        "preferred_experience": "2+ years"
    }

    def ats_score(resume, company):
        required = set(s.lower() for s in company["required_skills"])
        resume_skills = set(s.lower() for s in resume["skills"])
        matched = resume_skills & required
        score = round((len(matched) / len(required)) * 100, 2) if required else 0
        missing = list(required - matched)
        return {
            "match_score": score,
            "matched_skills": list(matched),
            "missing_skills": missing,
            "suggestion": "Consider adding: " + ", ".join(missing)
        }

    result = ats_score(resume_data, company_profile)

    st.subheader("📊 ATS Score & Suggestions")
    st.write("**Match Score:**", f"{result['match_score']}%")
    st.write("**Matched Skills:**", ", ".join(result["matched_skills"]))
    st.write("**Missing Skills:**", ", ".join(result["missing_skills"]))
    st.info(result["suggestion"])
else:
    st.info("⬆️ Please upload a resume file to begin.")
