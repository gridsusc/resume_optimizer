import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
import streamlit as st
import os
import tempfile
import json

# Assume these two functions are defined in another file you import
from convert_pdf_to_json import convert_pdf_to_json
from convert_json_to_pdf import convert_json_to_pdf
from template_retrival import set_chroma_db, get_related_template
from finetune import optimize_resume
from parse_resume import extract_relevant_json, update_relevant_json
from data.resume_templates import RESUME_TEMPLATES


st.title("Resume PDF ⇄ JSON Converter")
chroma_db=set_chroma_db(RESUME_TEMPLATES)
openai_key = st.text_input("Enter your OpenAI API Key", type="password")

uploaded_pdf = st.file_uploader("Upload a resume PDF", type="pdf")

if uploaded_pdf and openai_key:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded PDF
        pdf_path = os.path.join(tmpdir, "resume.pdf")
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())

        st.success("PDF uploaded successfully.")
        
        job_description= st.text_area("Enter Job Description", "Need a data scientist with experience in Python, SQL, and machine learning.")

        # Retrieve related templates
        related_templates = get_related_template(chroma_db,job_description)

        # Convert to JSON
        try:
            st.info("Converting PDF to JSON...")
            resume_json = convert_pdf_to_json(pdf_path, openai_key)

            # Save JSON to file
            with open("resume.json", "w") as f:
                json.dump(resume_json, f, indent=2)

            st.success("Converted PDF to JSON.")
            
            extract_relevant_json(resume_json) 
            optimize_resume("resume-prompt.json", related_templates, job_description, "optimized_resume.json")
            
            update_relevant_json("optimized_resume.json", "resume.json")
            # Convert back to PDF
            pdf_path = convert_json_to_pdf(resume_json)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, "resume.pdf", "application/pdf")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
