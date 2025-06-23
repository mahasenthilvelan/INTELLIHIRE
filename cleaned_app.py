#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#step 0 Logo + Splash Screen

import streamlit as st
import time

# Display Logo (upload 'logo.png' to the same folder or use a URL)
st.image("logo.png", width=250)  # ← #your_logo_path

# Animated Text
st.markdown("<h3 style='text-align: center;'>👋 Welcome to intellihire</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Your Smart ATS & HR Companion</h4>", unsafe_allow_html=True)

# Add a short delay to simulate splash screen effect
time.sleep(2)  # shows splash for 2 seconds

# Optional horizontal line before home screen starts
st.markdown("---")


# In[ ]:


#step 1 login
import streamlit as st

# Title
st.title("🔐 Welcome to intellihire")

st.subheader("Login to Continue")

# Tabs for Login Options (Phone removed)
login_method = st.radio("Choose login method:", ["Email", "Continue with Google"])

if login_method == "Email":
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login with Email"):
        if username and email and password:
            # In real use, verify from DB
            st.success(f"✅ Welcome {username}, you're logged in with email.")
        else:
            st.error("❌ Please fill all fields.")

elif login_method == "Continue with Google":
    st.info("🔗 Redirecting to Google OAuth (Feature to be implemented)")
    if st.button("Login with Google"):
        st.success("✅ Google login simulated (actual implementation uses Firebase or OAuth2).")


# In[ ]:

import streamlit as st
import fitz  # PyMuPDF
import docx2txt
import re
import spacy
import tempfile
import json

st.title("📄 Resume Parser")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

import streamlit as st
import tempfile
import fitz  # PyMuPDF
import docx2txt
import re
import spacy

st.title("📄 Resume Parser App")

uploaded_file = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        filename = tmp_file.name

    # Function: Extract text
    def extract_text(filename):
        if filename.endswith(".pdf"):
            doc = fitz.open(filename)
            text = ""
            for page in doc:
                text += page.get_text("text")
            return text
        elif filename.endswith(".docx"):
            return docx2txt.process(filename)
        else:
            return ""

    # Extract contact info
    def extract_contact(text):
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)
        phone = re.findall(r"\+?\d[\d\s\-]{8,}", text)
        return email[0] if email else "Not found", phone[0] if phone else "Not found"

    # Extract name using SpaCy NER
    def extract_name(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Not found"

    # Extract skills using SpaCy
    def extract_skills(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text.lower())
        skills = []
        common_skills = ['python', 'java', 'sql', 'machine learning', 'data analysis', 'communication', 'leadership']
        for token in doc:
            if token.text in common_skills:
                skills.append(token.text)
        return list(set(skills))

    # Run all
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

    # Show results
    st.subheader("📋 Extracted Resume Data")
    st.write("**Name:**", name)
    st.write("**Email:**", email)
    st.write("**Phone:**", phone)
    st.write("**Skills:**", ", ".join(skills))
    st.text_area("📝 Full Resume Text", text[:3000])
    st.subheader("📦 JSON Output")
    st.json(resume_data)

else:
    st.info("⬆️ Please upload a resume file to begin.")
    resume_data = {
        "name": "N/A",
        "email": "N/A",
        "phone": "N/A",
        "skills": []
    }
    st.subheader("📦 JSON Output")
    st.json(resume_data)


# In[ ]:


# Resume data from Step 1 (or use manually here)
# resume_data = {} # Removed this line

# Sample company profile (Amazon-style)
company_profile = {
    "company": "Amazon",
    "hiring_style": "Fast-paced, leadership-focused, deep tech",
    "required_skills": ["python", "java", "leadership", "machine learning", "communication"],
    "preferred_experience": "2+ years"
}

# ATS Scoring Logic
def ats_score(resume, company):
    required = set([s.lower() for s in company["required_skills"]])
    resume_skills = set([s.lower() for s in resume["skills"]])

    print("---Resume Skills Used for Scoring---")
    print(resume["skills"])
    print("---End of Resume Skills---")

    matched = resume_skills.intersection(required)
    # Handle division by zero if required skills is empty
    score = (len(matched) / len(required) * 100) if len(required) > 0 else 0

    missing = list(required - matched)

    feedback = {
        "match_score": round(score, 2),
        "matched_skills": list(matched),
        "missing_skills": missing,
        "suggestion": "Try adding experience with: " + ", ".join(missing)
    }

    return feedback

# Run the match
result = ats_score(resume_data, company_profile)

# Show result
import json
print(json.dumps(result, indent=2))


# In[ ]:





# In[ ]:



from pyngrok import ngrok

# Set your ngrok token directly
ngrok.set_auth_token("2ygEupQpveEWCPPm6X14z4s1CAA_7GpWHAh3HAtvTftdkqoQF")
streamlit_app_code ="""
import streamlit as st

st.title("Resume ATS Matcher")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")
    st.write("Resume processing and ATS scoring coming soon!")
"""

with open("app.py", "w") as f:
    f.write(streamlit_app_code)
import subprocess
import time

# Start streamlit
process = subprocess.Popen(['streamlit', 'run', 'app.py'])

# Wait a few seconds for Streamlit to start
time.sleep(10)

# Connect via ngrok
public_url = ngrok.connect(8501)
print("🔗 Your app is available at:", public_url)




# In[ ]:



import streamlit as st
import pdfplumber
import docx
import re

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

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")

    # Extract text based on file type
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        resume_text = ""

    # Display extracted info
    st.subheader("Parsed Resume Data")
    st.write("📧 Email:", extract_email(resume_text))
    st.text_area("📝 Full Resume Text", resume_text[:3000])  # Limit for display


# In[ ]:


def get_keywords(text):
    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

# Example job description
job_description = """
We are looking for a Python developer with experience in data analysis, Pandas, NumPy, and machine learning.
Strong problem-solving skills and knowledge of Flask or Django is a plus.
"""

if uploaded_file is not None:
    st.subheader("🔍 ATS Match Score")

    jd_keywords = get_keywords(job_description)
    resume_keywords = get_keywords(resume_text)

    # Intersection of resume and JD keywords
    matched = jd_keywords & resume_keywords
    match_score = round(len(matched) / len(jd_keywords) * 100)

    st.write("✅ Matched Keywords:", ", ".join(matched))
    st.write("🎯 Match Score:", f"{match_score}%")

    # Optionally: Show feedback
    if match_score >= 70:
        st.success("Great match! You're a strong fit for this job.")
    elif match_score >= 40:
        st.warning("Decent match. Consider tailoring your resume more.")
    else:
        st.error("Low match. Resume needs improvement.")




# In[ ]:


import textstat

def analyze_soft_signals(text):
    signals = {}

    # Leadership indicators
    leadership_words = ["led", "managed", "initiated", "coordinated", "supervised", "mentored"]
    leadership_count = sum(text.lower().count(word) for word in leadership_words)
    signals['Leadership Signals'] = leadership_count

    # Action verbs
    action_verbs = ["developed", "designed", "created", "implemented", "built", "executed"]
    action_count = sum(text.lower().count(word) for word in action_verbs)
    signals['Action Verbs'] = action_count

    # Readability score (Flesch Reading Ease)
    signals['Readability Score'] = round(textstat.flesch_reading_ease(text), 2)

    # Verbosity (average sentence length)
    signals['Average Sentence Length'] = round(textstat.avg_sentence_length(text), 2)

    return signals

if uploaded_file is not None:
    st.subheader("🧠 Soft Signal Analysis")
    soft_signals = analyze_soft_signals(resume_text)

    for k, v in soft_signals.items():
        st.write(f"{k}: {v}")

    # Basic interpretation
    if soft_signals['Leadership Signals'] >= 3:
        st.success("Strong leadership tone.")
    else:
        st.warning("Add more leadership-oriented language.")

    if soft_signals['Action Verbs'] >= 4:
        st.success("Good use of action verbs.")
    else:
        st.warning("Consider using more impactful action verbs.")




# In[ ]:


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

        # Example: Save to session (in real app, store in DB)
        st.session_state["registered_company"] = {
            "name": company_name,
            "location": location,
            "domain": core_domain,
            "qualifications": qualifications,
            "style": hiring_style,
            "interview_type": interview_type,
            "hr_logic": hr_logic
        }


# In[ ]:


import time

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

    # Show sample answer after delay
    if user_input == "":
        time.sleep(15)  # Wait 15 seconds before showing model answer
        sample_answer = f"Sample Answer: (e.g.) I am a self-motivated individual who enjoys working on innovative projects."
        st.info(sample_answer)
    else:
        st.success("Answer submitted.")

    # Save to history
    st.session_state.chat_history.append((q, user_input or sample_answer))


# In[ ]:


import difflib

def match_resume_to_company(resume_text, company_profiles):
    best_match = None
    highest_score = 0

    for company in company_profiles:
        required = company["qualifications"]
        score = difflib.SequenceMatcher(None, resume_text.lower(), required.lower()).ratio()

        if score > highest_score:
            highest_score = score
            best_match = company

    return best_match, highest_score

st.subheader("📌 Matching Resume to Company")

if uploaded_file is not None:
    # Simulate parsed resume text
    resume_text = "Python, Machine Learning, Flask, Streamlit, B.Tech in CS"

    # Load dummy company profiles
    company_profiles = [
        {"name": "AI Tech", "qualifications": "Python, AI, Flask", "domain": "AI"},
        {"name": "FinCore", "qualifications": "Finance, SQL, Excel", "domain": "FinTech"},
    ]

    matched_company, score = match_resume_to_company(resume_text, company_profiles)

    if score > 0.5:
        st.success(f"✅ Matched with: {matched_company['name']} (Score: {int(score*100)}%)")
        st.button("📤 Send Resume")
    else:
        st.warning("❌ No strong match found. Consider upskilling before retrying.")



# In[ ]:


import streamlit as st
import time

# Mock database for scheduled interviews by company (based on resume match)
interview_schedule = {
    "Anu": {
        "status": "selected",
        "slot": "2025-06-22, 10:30 AM",
        "company": "TechNova Solutions"
    },
    "Ravi": {
        "status": "rejected",
        "slot": None,
        "company": "TechNova Solutions"
    }
}

# HR AI Coaching Questions and Auto Answers (simulated)
mock_interview_questions = [
    {"question": "Tell me about yourself.", "answer": "Structure your answer using past experience, strengths, and career goals."},
    {"question": "Why should we hire you?", "answer": "Highlight your skills, achievements, and how they match the job role."},
    {"question": "Describe a challenge you faced and how you handled it.", "answer": "Use the STAR method: Situation, Task, Action, Result."},
    {"question": "What is your strength?", "answer": "Pick a relevant strength and give an example of how you used it."},
]

# UI starts here
st.title("🎯 Interview Scheduler & HR AI Coach")

name = st.text_input("Enter your full name to check your interview status")

if name:
    candidate = interview_schedule.get(name)
    if candidate:
        if candidate['status'] == "selected":
            st.success(f"✅ Congratulations! You are shortlisted by **{candidate['company']}**.")
            st.info(f"📅 Your Interview is scheduled for: **{candidate['slot']}**")

            st.divider()
            st.subheader("🤖 AI HR Coaching (Simulated Chat)")

            for idx, qa in enumerate(mock_interview_questions):
                st.write(f"**Q{idx+1}: {qa['question']}**")
                time.sleep(2)  # Delay to simulate waiting
                st.info(f"💡 Suggested Answer: {qa['answer']}")
        else:
            st.error("❌ Sorry, you were not shortlisted for this round.")
    else:
        st.warning("📡 HR is still reviewing your resume. Please check again later.")


# In[ ]:


import streamlit as st
import pandas as pd
import json

st.title("🏢 Company Dashboard")

# Dummy applicant data (replace with DB call)
applicants = [
    {"name": "John Doe", "match_score": 87, "status": "Pending", "skills": ["Python", "ML", "SQL"]},
    {"name": "Jane Smith", "match_score": 74, "status": "Shortlisted", "skills": ["Java", "DSA", "Leadership"]},
]

df = pd.DataFrame(applicants)
st.write("### Applicant List")
st.dataframe(df)

# Select an applicant to view
selected_name = st.selectbox("Select an applicant to view", [a["name"] for a in applicants])

# Show detailed info
for applicant in applicants:
    if applicant["name"] == selected_name:
        st.write("#### Resume Info")
        st.json(applicant)

        if st.button("Schedule Interview"):
            st.success("Interview Scheduled!")

        if st.button("Reject Candidate"):
            st.warning("Candidate Rejected.")


# In[ ]:


import streamlit as st
import random

st.title("🔐 Secure OTP Login")

login_method = st.radio("Choose login method:", ["Email", "Phone Number"])

# Generate and store OTP in session
if "otp" not in st.session_state:
    st.session_state.otp = None

if login_method == "Email":
    email = st.text_input("Enter your Email")
    if st.button("Send OTP"):
        if email:
            st.session_state.otp = str(random.randint(100000, 999999))
            st.info(f"📧 OTP sent to {email} (Simulated OTP: {st.session_state.otp})")
        else:
            st.warning("Enter a valid email.")

elif login_method == "Phone Number":
    phone = st.text_input("Enter your Mobile Number (+91...)")
    if st.button("Send OTP"):
        if phone:
            st.session_state.otp = str(random.randint(100000, 999999))
            st.info(f"📱 OTP sent to {phone} (Simulated OTP: {st.session_state.otp})")
        else:
            st.warning("Enter a valid phone number.")

otp_input = st.text_input("Enter OTP to verify")
if st.button("Verify OTP"):
    if otp_input == st.session_state.otp:
        st.success("✅ OTP Verified. Logged in successfully!")
    else:
        st.error("❌ Invalid OTP. Try again.")


# In[ ]:


# Step 12: Applicant Shortlisting & Status Management (Streamlit Version)

import streamlit as st
import pandas as pd

# Sample data (this would come from a real backend/database in production)
data = [
    {"Name": "Alice John", "Email": "alice@example.com", "Resume Score": 85, "Status": "Pending"},
    {"Name": "Bob Kumar", "Email": "bob@example.com", "Resume Score": 92, "Status": "Pending"},
    {"Name": "Carol Singh", "Email": "carol@example.com", "Resume Score": 76, "Status": "Pending"}
]

# Convert to DataFrame
df = pd.DataFrame(data)

st.title("📋 Applicant Review Dashboard")

for idx, row in df.iterrows():
    with st.expander(f"👤 {row['Name']} - {row['Email']}"):
        st.write(f"**Resume Score:** {row['Resume Score']}")
        st.write(f"**Current Status:** {row['Status']}")

        new_status = st.selectbox(
            f"Update status for {row['Name']}",
            ["Pending", "Shortlisted", "Interview Scheduled", "Rejected"],
            key=f"status_{idx}"
        )

        comment = st.text_area(f"Optional Comment on {row['Name']}:", key=f"comment_{idx}")

        if st.button(f"✅ Save status for {row['Name']}", key=f"save_{idx}"):
            df.at[idx, "Status"] = new_status
            st.success(f"Status updated to '{new_status}' for {row['Name']}")
            # In real case, update this in your database

st.write("\n---\n")
st.subheader("📊 Summary")
st.write(df[["Name", "Email", "Status"]])


# In[ ]:


import streamlit as st

# Mock list of shortlisted applicants
shortlisted_applicants = ["Alice Johnson", "Bob Singh", "Carla Mehta"]

st.title("HR Interview Feedback Submission")

# Select applicant
applicant = st.selectbox("Select Candidate", shortlisted_applicants)

# Input feedback
feedback = st.text_area("Enter Interview Feedback", height=150)

# Rating
rating = st.slider("Rate Candidate (1 = Poor, 5 = Excellent)", 1, 5)

# Submit button
if st.button("Submit Feedback"):
    # Here you would store the feedback in a database or a backend
    st.success(f"Feedback submitted for {applicant}")
    st.info(f"Rating: {rating}/5\nFeedback: {feedback}")


# In[ ]:


import streamlit as st
import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it)
conn = sqlite3.connect("applicant_feedback.db")
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        applicant_name TEXT,
        feedback TEXT,
        rating INTEGER,
        timestamp TEXT
    )
''')
conn.commit()

# Sample dynamic applicant list from database (mocking for now)
shortlisted_applicants = ["Alice Johnson", "Bob Singh", "Carla Mehta"]

st.title("HR Interview Feedback Submission")

# Select an applicant
applicant = st.selectbox("Select Candidate", shortlisted_applicants)

# Feedback text
feedback = st.text_area("Enter Interview Feedback", height=150)

# Rating slider
rating = st.slider("Rate Candidate (1 = Poor, 5 = Excellent)", 1, 5)

# Submit button
if st.button("Submit Feedback"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO feedback (applicant_name, feedback, rating, timestamp) VALUES (?, ?, ?, ?)",
              (applicant, feedback, rating, timestamp))
    conn.commit()
    st.success(f"✅ Feedback submitted for {applicant}")
    st.info(f"📝 Rating: {rating}/5\n📄 Feedback: {feedback}")

# View feedback table (optional)
if st.checkbox("Show Submitted Feedback"):
    c.execute("SELECT * FROM feedback")
    rows = c.fetchall()
    for row in rows:
        st.write(row)
# feedback_status.py



# In[ ]:


# 📘 Example Notebook: Flask + Ngrok + Streamlit (Full Setup)

# ✅ STEP 1: Install Requirements
get_ipython().system('pip install flask pyngrok streamlit -q')

# ✅ STEP 2: Create a simple Flask backend API
flask_code = '''
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/feedback", methods=["GET"])
def feedback():
    applicant_id = request.args.get("id", "101")
    return jsonify({
        "id": applicant_id,
        "company": "Dosa Inc.",
        "status": "Shortlisted",
        "feedback": "Excellent communication and technical skills."
    })

if __name__ == '__main__':
    app.run(port=5000)
'''

with open("backend.py", "w") as f:
    f.write(flask_code)

# ✅ STEP 3: Run Flask in background
import subprocess
subprocess.Popen(["python3", "backend.py"])

# ✅ STEP 4: Set up and start ngrok
from pyngrok import ngrok



ngrok.set_auth_token("2ygEupQpveEWCPPm6X14z4s1CAA_7GpWHAh3HAtvTftdkqoQF")  # <-- Replace with your real token
public_url = ngrok.connect(8501)
print("🔗 Flask is now public at:", public_url)

# ✅ STEP 5: Create Streamlit app that talks to Flask
streamlit_code = f'''
import streamlit as st
import requests

st.title("📄 Feedback Viewer")
id = st.text_input("Enter Applicant ID", value="101")

if st.button("Get Feedback"):
    response = requests.get("{public_url}/feedback", params={{"id": id}})
    if response.status_code == 200:
        data = response.json()
        st.success(f"Company: {{data['company']}}")
        st.write(f"Status: {{data['status']}}")
        st.write(f"Feedback: {{data['feedback']}}")
    else:
        st.error("Could not fetch data")
'''

with open("app.py", "w") as f:
    f.write(streamlit_code)

# ✅ STEP 6: Run Streamlit (in background)
subprocess.Popen(["streamlit", "run", "app.py"])

# ✅ Done!
print("✔️ Streamlit and Flask are running. Use the ngrok URL above to connect.")


# In[ ]:


import streamlit as st
import requests

# Use your public ngrok URL
API_URL = "https://9f30-34-125-10-157.ngrok-free.app"

st.title("📄 Resume ATS Matcher")

uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    if st.button("Check ATS Match"):
        files = {"resume": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/parse-resume", files={"file": (uploaded_file.name, uploaded_file, "multipart/form-data")})

        if response.status_code == 200:
            result = response.json()
            st.header("✅ ATS Feedback")
            st.write(f"**Match Score**: {result.get('score')}%")
            st.write(f"**Feedback**: {result.get('feedback')}")
        else:
            st.error("❌ Failed to connect to backend. Try again.")


# In[ ]:


from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/applicant/feedback", methods=["GET"])
def feedback():
    applicant_id = request.args.get("applicant_id")
    # Return dummy response
    return jsonify([{
        "company": "TechNova",
        "status": "Selected",
        "feedback": "Great communication skills"
    }])

app.run(port=1113)


# In[ ]:


from pyngrok import ngrok
public_url = ngrok.connect(1113)
print("🔗 PUBLIC URL:", public_url)


# In[ ]:


get_ipython().system('flask run --port=1113')


# In[ ]:


import requests
applicant_id = "101"
response = requests.get("https://9f30-34-125-10-157.ngrok-free.app/applicant/feedback", params={"applicant_id": applicant_id})

#OR


# In[ ]:


#this
# app_feedback_view.py
import streamlit as st
import requests

st.title("📄 My Interview Feedback & Status")

applicant_id = st.text_input("Enter your Applicant ID")

if st.button("View Feedback"):
    if applicant_id:
        response = requests.get("https://9f30-34-125-10-157.ngrok-free.app/applicant/feedback", params={"applicant_id": applicant_id})
        data = response.json()
        if data:
            for record in data:
                st.subheader(f"Company: {record['company']}")
                st.markdown(f"**Status:** {record['status']}")
                st.markdown(f"**Feedback:** {record['feedback']}")
                st.markdown("---")
        else:
            st.warning("No feedback found for this applicant.")
    else:
        st.error("Please enter your Applicant ID.")



# In[ ]:


#STEP 15
import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("resume_ats.db")
cursor = conn.cursor()

# USERS table: For login credentials
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT,
    password TEXT
)
""")

# COMPANIES table: Company registration info
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    style TEXT,
    required_skills TEXT,
    interview_status TEXT
)
""")

# APPLICANTS table: Resume and ATS score storage
cursor.execute("""
CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skills TEXT,
    ats_score REAL,
    resume_path TEXT
)
""")

# FEEDBACK table: HR/company feedback for applicants
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER,
    company_name TEXT,
    feedback TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()
print("✅ Database initialized successfully.")


# In[ ]:


# STEP 15 B
#INSERT  Data Example (Users, Applicants, Feedback)
import sqlite3

conn = sqlite3.connect("resume_ats.db")
cursor = conn.cursor()

# Insert a new user
cursor.execute("""
INSERT INTO users (name, username, email, phone, password)
VALUES (?, ?, ?, ?, ?)
""", ("Maha Lakshmi", "maha2025", "maha@gmail.com", "+919876543210", "secure123"))

# Insert a new applicant
cursor.execute("""
INSERT INTO applicants (name, skills, ats_score, resume_path)
VALUES (?, ?, ?, ?)
""", ("Maha Lakshmi", "python, sql, machine learning", 88.5, "resumes/maha.pdf"))

# Insert feedback
cursor.execute("""
INSERT INTO feedback (applicant_id, company_name, feedback, status)
VALUES (?, ?, ?, ?)
""", (1, "TechNova Solutions", "Very strong technical profile", "selected"))

conn.commit()
conn.close()
print("✅ Data inserted successfully.")


# In[ ]:


#STEP 15 C
#FETCH DATA EXAMPLE
import sqlite3

conn = sqlite3.connect("resume_ats.db")
cursor = conn.cursor()

# Fetch all applicants
cursor.execute("SELECT * FROM applicants")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()


# In[ ]:


#STREAMLIT Form: Insert into Users, Applicants, Feedback
import streamlit as st
import sqlite3

st.title("📥 Insert Resume & Feedback Info")

# Tabs for different inserts
tab1, tab2, tab3 = st.tabs(["👤 Add User", "📄 Add Applicant", "💬 Add Feedback"])

with tab1:
    st.header("👤 Register New User")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")

    if st.button("Add User"):
        conn = sqlite3.connect("resume_ats.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (name, username, email, phone, password) VALUES (?, ?, ?, ?, ?)",
                  (name, username, email, phone, password))
        conn.commit()
        conn.close()
        st.success("✅ User added successfully!")

with tab2:
    st.header("📄 Add New Applicant")
    a_name = st.text_input("Applicant Name")
    a_skills = st.text_input("Skills (comma separated)")
    ats_score = st.number_input("ATS Score", min_value=0.0, max_value=100.0)
    resume_path = st.text_input("Resume File Path")

    if st.button("Add Applicant"):
        conn = sqlite3.connect("resume_ats.db")
        c = conn.cursor()
        c.execute("INSERT INTO applicants (name, skills, ats_score, resume_path) VALUES (?, ?, ?, ?)",
                  (a_name, a_skills, ats_score, resume_path))
        conn.commit()
        conn.close()
        st.success("✅ Applicant added successfully!")

with tab3:
    st.header("💬 Submit Feedback")
    applicant_id = st.number_input("Applicant ID", step=1)
    company_name = st.text_input("Company Name")
    feedback = st.text_area("Feedback Message")
    status = st.selectbox("Status", ["selected", "rejected", "pending"])

    if st.button("Submit Feedback"):
        conn = sqlite3.connect("resume_ats.db")
        c = conn.cursor()
        c.execute("INSERT INTO feedback (applicant_id, company_name, feedback, status) VALUES (?, ?, ?, ?)",
                  (applicant_id, company_name, feedback, status))
        conn.commit()
        conn.close()
        st.success("✅ Feedback submitted successfully!")


# In[ ]:


#step 15
import streamlit as st
import sqlite3

# Connect to DB
def get_connection():
    return sqlite3.connect("resume_ats.db")

# Create table if it doesn't exist
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id TEXT,
            company_name TEXT,
            feedback TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

# Title
st.title("📬 HR Feedback Manager")

# Submit form
with st.form("feedback_form"):
    st.subheader("➕ Submit New Feedback")
    applicant_id = st.text_input("Applicant ID")
    company_name = st.text_input("Company Name")
    feedback_text = st.text_area("Feedback")
    status = st.selectbox("Status", ["selected", "rejected", "pending"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        if applicant_id and company_name and feedback_text:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (applicant_id, company_name, feedback, status)
                VALUES (?, ?, ?, ?)
            """, (applicant_id, company_name, feedback_text, status))
            conn.commit()
            conn.close()
            st.success("✅ Feedback submitted successfully!")
        else:
            st.warning("❗ Please fill all fields.")

# Show all feedbacks
st.subheader("📄 All Feedback Records")

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM feedback")
rows = cursor.fetchall()
conn.close()

for row in rows:
    st.markdown(f"🆔 ID: `{row[0]}` | 👤 Applicant: `{row[1]}` | 🏢 Company: `{row[2]}`")
    st.markdown(f"📌 Status: `{row[4]}`")
    st.markdown(f"📝 Feedback: {row[3]}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"✏️ Edit", key=f"edit_{row[0]}"):
            with st.form(f"edit_form_{row[0]}"):
                new_feedback = st.text_area("Edit Feedback", row[3])
                new_status = st.selectbox("Edit Status", ["selected", "rejected", "pending"], index=["selected", "rejected", "pending"].index(row[4]))
                update = st.form_submit_button("Update")

                if update:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE feedback
                        SET feedback = ?, status = ?
                        WHERE id = ?
                    """, (new_feedback, new_status, row[0]))
                    conn.commit()
                    conn.close()
                    st.success("✅ Feedback updated. Please refresh the page.")

    with col2:
        if st.button(f"🗑️ Delete", key=f"delete_{row[0]}"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM feedback WHERE id = ?", (row[0],))
            conn.commit()
            conn.close()
            st.warning("⚠️ Feedback deleted. Please refresh the page.")


# In[ ]:


# Define resume_data (normally this is extracted earlier from uploaded resume)
resume_data = {
    "name": "Anu",
    "email": "maha@example.com",
    "phone": "1234567890",
    "skills": ["python", "data analysis", "machine learning"]
}

# Define company_profile (normally set based on selected company)
company_profile = {
    "company": "TechNova",
    "required_skills": ["python", "java", "leadership", "machine learning"]
}


# In[ ]:


#STEP 16
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample extracted resume skills
resume_skills = resume_data.get("skills", ["python", "data analysis", "machine learning"])
company_skills = company_profile.get("required_skills", ["python", "java", "leadership", "machine learning"])

# Combine both into documents
documents = [" ".join(resume_skills), " ".join(company_skills)]

# Compute TF-IDF vectors
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Compute similarity
similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
score_percent = round(similarity[0][0] * 100, 2)

# Display result
print("🎯 TF-IDF Cosine Similarity Score:", score_percent, "%")


# In[ ]:


#Step 16: TF-IDF Skill Matching into your Streamlit UI
#Streamlit Code for TF-IDF Similarity Score



import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("📊 TF-IDF Resume Matching")

# Example data – replace with real resume_data and company_profile
resume_skills = st.text_area("Paste Extracted Resume Skills (space-separated)", "python data analysis machine learning")
company_skills = st.text_area("Paste Company Required Skills (space-separated)", "python java leadership machine learning")

if st.button("Compare Skills (TF-IDF Match)"):
    try:
        documents = [resume_skills, company_skills]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = round(similarity[0][0] * 100, 2)

        st.success(f"✅ TF-IDF Cosine Similarity Score: {score}%")

        if score > 75:
            st.info("🔍 Strong match! Resume aligns well with company expectations.")
        elif score > 50:
            st.warning("⚠️ Moderate match. Consider improving resume skill alignment.")
        else:
            st.error("❌ Weak match. Skills don't align well with job requirements.")
    except:
        st.error("Something went wrong. Please check your input.")


# In[ ]:


#step 17


# In[ ]:


#step 17
import streamlit as st
import pyrebase

firebase_config = {
    "apiKey": "AIzaSyBWDSUUJO9rnmaeHw0m6UHvzX_F3MOx70Y",
    "authDomain": "your-project.firebaseapp.com",
    "projectId": "your-project",
    "storageBucket": "your-project.appspot.com",
    "messagingSenderId": "SENDER_ID",
    "appId": "APP_ID",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

st.title("🔐 Login with Google (Firebase Auth)")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success(f"Welcome, {email}")
    except:
        st.error("Login failed. Check credentials.")


# In[ ]:


#step 17 #step 17  connect your Firebase project to Streamlit using Python
#step 2  Use Your Firebase Config in Python
import streamlit as st
import pyrebase

# ✅ Replace these values with your Firebase config
firebaseConfig = {
    "apiKey": "AIzaSyBWDSUUJO9rnmaeHw0m6UHvzX_F3MOx70Y",
    "authDomain": "your-project-id.firebaseapp.com",
    "projectId": "your-project-id",
    "storageBucket": "your-project-id.appspot.com",
    "messagingSenderId": "1234567890",
    "appId": "1:1234567890:web:abcdef123456",
    "databaseURL": ""  # Optional
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


# In[ ]:


# Firebase Google Sign-In Simulation with Email/Password fallback (Streamlit)
# both Integrated (REAL) & Simulated (FAKE)
import streamlit as st
import pyrebase

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyBWDSUUJO9rnmaeHw0m6UHvzX_F3MOx70Y",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com",
    "messagingSenderId": "SENDER_ID",
    "appId": "APP_ID",
    "measurementId": "G-MEASUREMENT_ID",
    "databaseURL": ""
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Streamlit UI
st.title("🔐 AI Resume Sculptor Login")
login_option = st.radio("Choose Login Method", ["Email/Password", "Google (Simulated)"])

if login_option == "Email/Password":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)#integrated(real)
            st.success(f"✅ Logged in as {email}")
        except:
            st.error("❌ Invalid email or password.")
#smiulated(login)
elif login_option == "Google (Simulated)":
    st.info("🔗 In real apps, Google Sign-In uses Firebase OAuth or popup in web apps.")
    if st.button("Continue with Google"):
        st.success("✅ Simulated Google login complete (for prototype/demo only).")

# Optional: Add logout or session state handling


# In[ ]:


#step 17 #step 17  connect your Firebase project to Streamlit using Python
#Step 3: Streamlit Login UI with Firebase Authentication
st.title("🔐 Login with Firebase (Email Only)")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success("✅ Login Successful!")
        st.write("Welcome, UID:", user['localId'])
    except:
        st.error("❌ Invalid email or password.")


# In[ ]:


#step 17 connect your Firebase project to Streamlit using Python
#step 4  Optional: Sign Up (Firebase)
if st.button("Sign Up"):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        st.success("✅ User Created!")
    except:
        st.error("⚠️ Account already exists or invalid details.")


# In[ ]:


#Step 18: OTP via SendGrid or Twilio (Optional for Production Use)
#step 1


# In[ ]:


# In[ ]:


# Step 18: OTP via MailSlurp
import streamlit as st
import random
import time
from mailslurp_client import Configuration, ApiClient, InboxControllerApi, SendEmailOptions

# 🟨 Your API key here from MailSlurp
MAILSLURP_API_KEY = "250a10842e4aa9f1fc351ad7717d240dcae868bcb14086d14bfd88dfb3d657a5"  # ← #your_api_key

# 🟨 OTP storage for verification
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = ""

# 🟨 Configure MailSlurp client
configuration = Configuration()
configuration.api_key["x-api-key"] ="250a10842e4aa9f1fc351ad7717d240dcae868bcb14086d14bfd88dfb3d657a5"# ← #your_api_key
api_client = ApiClient(configuration)
inbox_api = InboxControllerApi(api_client)

# 🟩 Create a new inbox
st.title("📧 OTP Login via MailSlurp")

if "email_address" not in st.session_state:
    inbox = inbox_api.create_inbox()
    st.session_state.inbox_id = inbox.id
    st.session_state.email_address = inbox.email_address

st.info(f"Temporary Login Email: **{st.session_state.email_address}**")  # ← #your_email

# 🟨 Send OTP
if st.button("Send OTP"):
    otp = str(random.randint(100000, 999999))
    st.session_state.generated_otp = otp

    send_options = SendEmailOptions(
        to=[st.session_state.email_address],
        subject="Your OTP Code",
        body=f"Your one-time password is: {otp}"
    )

    inbox_api.send_email(inbox_id=st.session_state.inbox_id, send_email_options=send_options)
    st.success("✅ OTP sent to your MailSlurp email inbox.")

# 🟩 Display field to input OTP
entered_otp = st.text_input("Enter OTP")

if st.button("Verify OTP"):
    if entered_otp == st.session_state.generated_otp:
        st.success("🎉 OTP Verified! You’re logged in.")
    else:
        st.error("❌ Incorrect OTP. Please try again.")


# In[ ]:


#step 19 HR Feedback Form (Manual Entry with Streamlit + SQLite)
#step 1
import streamlit as st
import sqlite3

# Connect to DB
def get_connection():
    return sqlite3.connect("resume_ats.db")

# Streamlit Form UI
st.title("📬 HR Feedback Submission")

applicant_id = st.text_input("🆔 Applicant ID")
company_name = st.text_input("🏢 Company Name")
feedback_text = st.text_area("📝 Feedback")
status = st.selectbox("📌 Status", ["selected", "rejected", "pending"])

if st.button("✅ Submit Feedback"):
    if applicant_id and company_name and feedback_text:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback (applicant_id, company_name, feedback, status)
            VALUES (?, ?, ?, ?)
        """, (applicant_id, company_name, feedback_text, status))
        conn.commit()
        conn.close()
        st.success("🎉 Feedback submitted successfully!")
    else:
        st.warning("❗ Please fill all fields before submitting.")


# In[ ]:


#step 19 #step 19 HR Feedback Form (Manual Entry with Streamlit + SQLite)

#step 2 filter feedback by applicant ID or company name using Streamlit and SQLite.

import streamlit as st
import sqlite3
import pandas as pd

# Connect to DB
def get_connection():
    return sqlite3.connect("resume_ats.db")

st.title("🔎 HR Feedback Viewer")

# Filters
search_by = st.radio("Filter by:", ["Applicant ID", "Company Name"])

if search_by == "Applicant ID":
    applicant_id = st.text_input("Enter Applicant ID")
    query = "SELECT * FROM feedback WHERE applicant_id = ?" if applicant_id else "SELECT * FROM feedback"
    params = (applicant_id,) if applicant_id else ()
else:
    company_name = st.text_input("Enter Company Name")
    query = "SELECT * FROM feedback WHERE company_name = ?" if company_name else "SELECT * FROM feedback"
    params = (company_name,) if company_name else ()

# Fetch and show
if st.button("🔍 Show Feedback"):
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("No feedback found.")


# In[ ]:


#create the feedback table

import sqlite3

conn = sqlite3.connect("resume_ats.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER,
    company_name TEXT,
    feedback TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()
print("✅ feedback table created.")


# In[ ]:


#sample feedback entries
import sqlite3

conn = sqlite3.connect("resume_ats.db")
cur = conn.cursor()

sample_data = [
    (101, "ankh cybernetic", "Great leadership and Python skills.", "selected"),
    (102, "DataCrafters", "Good data analysis, but needs more ML exposure.", "pending"),
    (103, "CloudWorks Inc.", "Lacks communication skills.", "rejected")
]

cur.executemany("""
INSERT INTO feedback (applicant_id, company_name, feedback, status)
VALUES (?, ?, ?, ?)
""", sample_data)

conn.commit()
conn.close()

print("✅ Sample feedback entries inserted.")


# In[ ]:


##step 19 #step 19 HR Feedback Form (Manual Entry with Streamlit + SQLite)
#step 3 edit and delete options to your Streamlit feedback viewer
import streamlit as st
import sqlite3
import pandas as pd

# DB connection
def get_connection():
    return sqlite3.connect("resume_ats.db")

st.title("✏️ Feedback Manager")

# Show all feedback entries
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM feedback", conn)
conn.close()

if df.empty:
    st.warning("No feedback available.")
else:
    st.dataframe(df)

    # Select row to edit/delete
    selected_id = st.selectbox("Select Feedback ID to Edit/Delete", df['id'])

    # Fetch the selected row
    row = df[df['id'] == selected_id].iloc[0]

    # Editable fields
    new_company = st.text_input("Company Name", row["company_name"])
    new_feedback = st.text_area("Feedback", row["feedback"])
    new_status = st.selectbox("Status", ["selected", "rejected", "pending"], index=["selected", "rejected", "pending"].index(row["status"]))

    # Buttons
    if st.button("💾 Update"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE feedback
            SET company_name = ?, feedback = ?, status = ?
            WHERE id = ?
        """, (new_company, new_feedback, new_status, selected_id))
        conn.commit()
        conn.close()
        st.success("Feedback updated successfully.")

    if st.button("🗑️ Delete"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM feedback WHERE id = ?", (selected_id,))
        conn.commit()
        conn.close()
        st.success("Feedback deleted successfully.")


# In[ ]:


from pyngrok import ngrok

# 🔑 Set your ngrok token
ngrok.set_auth_token("2ygEupQpveEWCPPm6X14z4s1CAA_7GpWHAh3HAtvTftdkqoQF")  # 👈 GIVE YOURS (Get from https://dashboard.ngrok.com)

# 📦 Define your project requirements
requirements = [
    "datetime",
    "difflib",
    "docx",
    "docx2txt",
    "dotenv",
    "pymupdf",
    "flask",
    "google",
    "json",
    "mailslurp_client",
    "openai",
    "os",
    "pandas",
    "pdfplumber",
    "pymongo",
    "pyngrok",
    "pyrebase",
    "pyrebase4",
    "random",
    "re",
    "requests",
    "sklearn",
    "spacy", 
    "sqlite3",
    "streamlit",
    "sendgrid",
    "subprocess",
    "textstat",
    "time",
    "ngrok",
    "streamlit -q",
    "jsonify",
    "TfidfVectorizer",
    "cosine_similarity",
    "mailslurp-client",
    "dotenv"    
]
# ✅ You can add or remove packages based on your actual usage
# Example: remove `flask` if not used in your app
readme_path = "/content/README (2).md"  # 👈 Change this if you want to save to a different location
config_path = "/content/config (1).toml" # 👈 Streamlit config file path

# 📝 README description
with open(readme_path, "w", encoding="utf-8") as f:
    f.write("# IntelliHire\n\nThis app simulates an AI-powered resume screening system with ATS scoring, HR Q&A simulation, feedback tracking, and interview scheduling.\n")
    # 👈 CHANGE this description if you want to customize the README

# 🌐 Streamlit config (Optional - leave as-is unless port conflicts)
with open(config_path, "w", encoding="utf-8") as f:
    f.write("[server]\nheadless = true\nenableCORS = false\nport = 1112\n")
    # 👈 CHANGE port (8501) only if needed (e.g., port already in use)


# In[ ]:




# In[ ]:


#Create app.py with Your Streamlit Code
import streamlit as st

st.title("🎯 IntelliHire - AI Resume Screener")
st.write("Welcome to IntelliHire! Upload your resume to get started.")
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
if uploaded_file:
    st.success("Resume uploaded successfully.")


# In[ ]:


#Launch the Streamlit App


# In[ ]:




# In[ ]:


public_url = ngrok.connect(1113)
print("Your public app URL:", public_url)


# In[ ]:


with open("cleaned_app.py", "w") as f:
    f.write("""

import streamlit as st

st.set_page_config(page_title="IntelliHire", layout="centered")

st.title("🤖 IntelliHire – AI Resume Screener")
st.markdown("Upload your resume to simulate ATS scoring and HR screening.")

uploaded_file = st.file_uploader("📄 Upload your Resume", type=["pdf", "docx"])

if uploaded_file:
    st.success(f"✅ {uploaded_file.name} uploaded!")
    st.info("Processing will be added here in the full app.")
""")


# In[ ]:


import streamlit as st

st.set_page_config(page_title="IntelliHire", layout="centered")

st.title("🤖 IntelliHire – AI Resume Screener")
st.markdown("Upload your resume to simulate ATS scoring and HR screening.")

uploaded_file = st.file_uploader("📄 Upload your Resume", type=["pdf", "docx"])

if uploaded_file:
    st.success(f"✅ {uploaded_file.name} uploaded!")
    st.info("Processing will be added here in the full app.")


# In[ ]:


#create mongo Db


# In[ ]:


import streamlit as st
import pdfplumber
import docx2txt
import openai
from pymongo import MongoClient
import os

# ----------- 🔐 API Keys and Config -----------
openai.api_key = "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"  # 👈 Replace with your OpenAI API key
mongo_uri = "mongodb+srv://mahalakshmisenthilvelan:<db_password>@maha-intellihire-cluste.9lajg8j.mongodb.net/?retryWrites=true&w=majority&appName=maha-intellihire-cluster"          # 👈 Replace with your MongoDB URI if saving

# ----------- 💽 MongoDB Setup -----------
try:
    client = MongoClient(mongo_uri)
    db = client["intellihire"]
    collection = db["resumes"]
except:
    collection = None

# ----------- 📄 Extract Resume Text -----------
def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file.name.endswith(".docx"):
        with open("temp.docx", "wb") as f:
            f.write(file.read())
        text = docx2txt.process("temp.docx")
        os.remove("temp.docx")
    return text.strip()

# ----------- 📊 Simple ATS Scoring -----------
def score_resume(text):
    keywords = ["python", "machine learning", "data", "project", "team", "AI", "communication"]
    score = sum([kw.lower() in text.lower() for kw in keywords])
    return (score / len(keywords)) * 100

# ----------- 🤖 HR Q&A Simulation -----------
def generate_hr_questions(text):
    prompt = f"You are an HR manager. Read the following resume content and ask 3 interview questions:\n\n{text}\n\nQuestions:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ----------- 🌐 Streamlit UI -----------
st.set_page_config(page_title="IntelliHire", layout="centered")
st.title("🤖 IntelliHire – AI Resume Screener")
st.markdown("Upload your resume to simulate ATS scoring and HR screening.")

uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    resume_text = extract_text(uploaded_file)

    if resume_text:
        st.subheader("📄 Extracted Resume Text")
        st.text_area("Resume Content", resume_text, height=300)

        # ATS Scoring
        score = score_resume(resume_text)
        st.subheader("📊 ATS Score")
        st.metric(label="Match Score", value=f"{score:.2f} %")

        # HR Questions
        st.subheader("🧠 Simulated HR Questions")
        questions = generate_hr_questions(resume_text)
        st.write(questions)

        # Save to MongoDB
        if collection:
            save_data = {
                "filename": uploaded_file.name,
                "text": resume_text,
                "ats_score": score,
                "hr_questions": questions
            }
            collection.insert_one(save_data)
            st.success("📁 Resume saved to database.")
        else:
            st.warning("⚠️ MongoDB not connected. Resume not saved.")
    else:
        st.error("❌ Could not extract text from the resume.")


# In[ ]:


mongo_uri = "mongodb+srv://mahalakshmisenthilvelan:mahasenthilvelan@maha-intellihire-cluste.9lajg8j.mongodb.net/?retryWrites=true&w=majority&appName=maha-intellihire-cluster"


# In[ ]:




# In[ ]:


from dotenv import load_dotenv
load_dotenv()
openai.api_key ="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"


# In[ ]:



