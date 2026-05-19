import streamlit as st
import pdfplumber
import pandas as pd
import re
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Streamlit Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

st.write("Upload your resume PDF for ATS analysis")

# Skills Database
skills_db = {
    "Data Science": [
        "python",
        "sql",
        "machine learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "power bi",
        "tableau",
        "excel",
        "data analysis",
        "streamlit"
    ],

    "Web Development": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "mongodb",
        "express",
        "git",
        "github"
    ]
}

# PDF Text Extraction
def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

# Skill Extraction
def extract_skills(text, skills_list):

    found_skills = []

    text = text.lower()

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills

# ATS Score Calculation
def calculate_score(found_skills, total_skills):

    score = (len(found_skills) / len(total_skills)) * 100

    return round(score, 2)

# File Upload
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    # Extract Text
    resume_text = extract_text(uploaded_file)

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )

    # Role Selection
    selected_role = st.selectbox(
        "Select Job Role",
        list(skills_db.keys())
    )

    required_skills = skills_db[selected_role]

    # Extract Skills
    found_skills = extract_skills(
        resume_text,
        required_skills
    )

    # Missing Skills
    missing_skills = list(
        set(required_skills) - set(found_skills)
    )

    # ATS Score
    ats_score = calculate_score(
        found_skills,
        required_skills
    )

    # Display ATS Score
    st.subheader("ATS Score")

    st.metric(
        label="Resume ATS Score",
        value=f"{ats_score}%"
    )

    # Display Found Skills
    st.subheader("Detected Skills")

    st.write(found_skills)

    # Display Missing Skills
    st.subheader("Missing Skills")

    st.write(missing_skills)

    # Suggestions
    st.subheader("Suggestions")

    if ats_score >= 80:
        st.success("Excellent resume for this role.")

    elif ats_score >= 50:
        st.warning("Good resume but can be improved.")

    else:
        st.error("Resume needs significant improvement.")

    # Download Report
    report = pd.DataFrame({
        "Detected Skills": pd.Series(found_skills),
        "Missing Skills": pd.Series(missing_skills)
    })

    csv = report.to_csv(index=False)

    st.download_button(
        label="Download Analysis Report",
        data=csv,
        file_name="resume_analysis.csv",
        mime="text/csv"
    )