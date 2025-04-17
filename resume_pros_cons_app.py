import streamlit as st
from textblob import TextBlob
import pandas as pd
import fitz  # PyMuPDF
from fpdf import FPDF
import io

st.set_page_config(page_title="Resume Pros & Cons Analyzer", layout="centered")

st.title("📄 Resume Analyzer - Pros, Cons & Score")
st.write("Upload a resume PDF or paste text below to analyze its strengths and weaknesses.")

# --- Helper Functions ---

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def analyze_resume_text(text):
    pros = []
    cons = []
    score = 0

    if any(skill in text.lower() for skill in ["python", "java", "sql", "html", "css", "machine learning", "data analysis"]):
        pros.append("Mentions strong technical skills")
        score += 2
    else:
        cons.append("Technical skills not clearly mentioned")

    if "project" in text.lower() or "developed" in text.lower():
        pros.append("Describes project experience")
        score += 2
    else:
        cons.append("No mention of projects")

    if any(soft in text.lower() for soft in ["team", "communication", "leadership", "problem solving", "collaboration"]):
        pros.append("Highlights soft skills")
        score += 1
    else:
        cons.append("Soft skills not highlighted")

    if any(edu in text.lower() for edu in ["bachelor", "degree", "university", "college"]):
        pros.append("Includes educational qualifications")
        score += 1
    else:
        cons.append("Education details are missing")

    if "internship" in text.lower() or "experience" in text.lower() or "worked at" in text.lower():
        pros.append("Mentions work or internship experience")
        score += 2
    else:
        cons.append("No work or internship experience mentioned")

    blob = TextBlob(text)
    grammar_errors = sum(1 for sentence in blob.sentences if sentence.correct() != sentence)
    if grammar_errors < 3:
        pros.append("Grammatically sound content")
        score += 2
    else:
        cons.append("Contains grammatical errors")

    return pros, cons, score

def generate_pdf_report(pros, cons, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Resume Score: {score}/10", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(200, 10, txt="✅ Pros:", ln=True)
    pdf.set_font("Arial", "", 11)
    for p in pros:
        pdf.cell(200, 10, txt=f"- {p}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(200, 10, txt="❌ Cons:", ln=True)
    pdf.set_font("Arial", "", 11)
    for c in cons:
        pdf.cell(200, 10, txt=f"- {c}", ln=True)

    return pdf.output(dest='S').encode('latin-1')

# --- Interface ---

uploaded_file = st.file_uploader("📤 Upload your resume as PDF", type=["pdf"])
resume_text = st.text_area("📝 Or paste your resume text here", height=300)

analyze_btn = st.button("🔍 Analyze Resume")

if analyze_btn:
    final_text = ""

    if uploaded_file:
        final_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ Text extracted from uploaded PDF.")
    elif resume_text.strip():
        final_text = resume_text
    else:
        st.warning("Please upload a PDF or paste resume text.")
    
    if final_text:
        pros, cons, score = analyze_resume_text(final_text)

        st.markdown("### ✅ Pros vs ❌ Cons")
        df = pd.DataFrame({
            "✅ Pros": pros + [""] * (max(len(pros), len(cons)) - len(pros)),
            "❌ Cons": cons + [""] * (max(len(pros), len(cons)) - len(cons)),
        })
        st.table(df)

        st.markdown(f"### 🧮 Resume Score: `{score}/10`")

        if st.button("📥 Download Report as PDF"):
            pdf_bytes = generate_pdf_report(pros, cons, score)
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )
