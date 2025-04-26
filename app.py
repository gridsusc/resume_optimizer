# import streamlit as st
# import os
# import tempfile
# import json

# # Assume these two functions are defined in another file you import
# from convert_pdf_to_json import convert_pdf_to_json
# from convert_json_to_pdf import convert_json_to_pdf

# st.title("Resume PDF ⇄ JSON Converter")

# openai_key = st.text_input("Enter your OpenAI API Key", type="password")

# uploaded_pdf = st.file_uploader("Upload a resume PDF", type="pdf")

# if uploaded_pdf and openai_key:
#     with tempfile.TemporaryDirectory() as tmpdir:
#         # Save uploaded PDF
#         pdf_path = os.path.join(tmpdir, "resume.pdf")
#         with open(pdf_path, "wb") as f:
#             f.write(uploaded_pdf.read())

#         st.success("PDF uploaded successfully.")

#         # Convert to JSON
#         try:
#             st.info("Converting PDF to JSON...")
#             resume_json = convert_pdf_to_json(pdf_path, openai_key)

#             # Save JSON to file
#             json_path = os.path.join(tmpdir, "resume.json")
#             with open(json_path, "w") as f:
#                 json.dump(resume_json, f, indent=2)

#             st.success("Converted to JSON.")

#             # Convert back to PDF
#             output_pdf_path = os.path.join(tmpdir, "final_resume.pdf")
#             convert_json_to_pdf(json_path, output_pdf_path)

#             # Download button
#             with open(output_pdf_path, "rb") as f:
#                 st.download_button(
#                     label="Download Final Resume PDF",
#                     data=f,
#                     file_name="resume.pdf",
#                     mime="application/pdf"
#                 )

#         except Exception as e:
#             st.error(f"Something went wrong: {e}")
import streamlit as st
import json
from convert_json_to_pdf import convert_json_to_pdf

st.title("Resume PDF Generator")

uploaded_file = st.file_uploader("Upload your resume.json", type=["json"])
if uploaded_file:
    resume_json = json.load(uploaded_file)
    pdf_path = convert_json_to_pdf(resume_json)
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, "resume.pdf", "application/pdf")

