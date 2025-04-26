import json
import re
import pdfplumber
import os
from typing import Dict
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

basics_schema = '''{
    "name": "",
    "label": "",
    "image": "",
    "email": "",
    "phone": "",
    "url": "",
    "summary": "",
    "location": {
        "address": "",
        "postalCode": "",
        "city": "",
        "countryCode": "",
        "region": ""
    },
    "profiles": [
        {
            "network": "",
            "username": "",
            "url": ""
        }
    ]
}'''

work_schema = '''[
    {
        "name": "",
        "location": "",
        "description": "",
        "position": "",
        "url": "",
        "startDate": "",
        "endDate": "",
        "summary": "",
        "highlights": []
    }
]'''

education_schema = '''[
    {
        "institution": "",
        "url": "",
        "area": "",
        "studyType": "",
        "startDate": "",
        "endDate": "",
        "score": "",
        "courses": []
    }
]'''

skills_schema = '''[
    {
        "name": "",
        "level": "",
        "keywords": []
    }
]'''

projects_schema = '''[
    {
        "name": "",
        "description": "",
        "highlights": [],
        "keywords": [],
        "startDate": "",
        "endDate": "",
        "url": "",
        "roles": [],
        "entity": "",
        "type": ""
    }
]'''

def extract_json_object(response: str) -> str:
    """
    Extracts the JSON substring from the LLM response.
    """
    match = re.search(r'(\{.*\})', response, re.DOTALL)
    if match:
        return match.group(1)
    return response

def extract_json_array(response: str) -> str:
    """
    Extracts the JSON array substring from the LLM response.
    """
    match = re.search(r'(\[.*\])', response, re.DOTALL)
    if match:
        return match.group(1)
    return response

def convert_pdf_to_json(pdf_filepath: str, openai_key: str) -> Dict:
    pdf_text = ''
    with pdfplumber.open(pdf_filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text += page_text + '\n'

    basics_extracted = pdf_text.split('SKILLS AND TECH')[0]
    skills_extracted = pdf_text.split('EXPERIENCE')[0].split('SKILLS AND TECH')[1]
    work_extracted = pdf_text.split('VOLUNTEERING')[0].split('EXPERIENCE')[1]
    projects_extracted = pdf_text.split('EDUCATION')[0].split('PROJECTS')[1]
    education_extracted = pdf_text.split('PUBLICATIONS')[0].split('EDUCATION')[1]

    os.environ["OPENAI_API_KEY"] = openai_key
    llm = ChatOpenAI(temperature=0, model="gpt-4o") 

    conversion_prompt = (
        "Convert the extracted text into a JSON object or array that strictly adheres to the provided JSON schema. "
        "Use only the information present in the text; for any field not mentioned, set its value to an empty string. "
        "Output only the JSON array with no extra commentary or code.\n"
        "### Schema:\n{schema}\n"
        "### Extracted Text:\n{text}"
    )

    conversion_chain = (
        {"text": RunnablePassthrough(), "schema": RunnablePassthrough()}
        | ChatPromptTemplate.from_template(conversion_prompt)
        | llm
        | StrOutputParser()
    )

    basics_json_response = conversion_chain.invoke({"text": basics_extracted, "schema": basics_schema})
    basics_json_parsed = json.loads(extract_json_object(basics_json_response))

    work_json_response = conversion_chain.invoke({"text": work_extracted, "schema": work_schema})
    work_json_parsed = json.loads(extract_json_array(work_json_response))

    education_json_response = conversion_chain.invoke({"text": education_extracted, "schema": education_schema})
    education_json_parsed = json.loads(extract_json_array(education_json_response))

    skills_json_response = conversion_chain.invoke({"text": skills_extracted, "schema": skills_schema})
    skills_json_parsed = json.loads(extract_json_array(skills_json_response))

    projects_json_response = conversion_chain.invoke({"text": projects_extracted, "schema": projects_schema})
    projects_json_parsed = json.loads(extract_json_array(projects_json_response))

    resume_json = {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": basics_json_parsed,
        "work": work_json_parsed,
        "education": education_json_parsed,
        "skills": skills_json_parsed,
        "projects": projects_json_parsed,
        "meta": {
            "canonical": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/sample.resume.json",
            "version": "v1.0.0",
            "lastModified": "2017-12-24T15:53:00"
        }
    }

    return resume_json

if __name__ == '__main__':
    from getpass import getpass
    openai_key = getpass("OpenAI Key: ")
    pdf_path = 'data/Richard Hendriks.pdf'

    payload = convert_pdf_to_json(pdf_path, openai_key)
    print(json.dumps(payload, indent=4))
