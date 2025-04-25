# Import required libraries

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
import json
import os



model = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # or "gpt-4" for more advanced capabilities
    temperature=0.1,
)

# Obtain job description
from job_description import JOB_DESCRIPTION
job_description = JOB_DESCRIPTION

# Open and load the JSON file that used for template
with open('resume-prompt.json', 'r') as file:
    json_prompt = json.load(file)
raw_resume_text = json.dumps(json_prompt, indent=2).replace("{", "{{").replace("}", "}}")

# import the examples needed for few shot prompting
from examples import RESUME_EXAMPLES

# Example formatting for few-shot examples
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=RESUME_EXAMPLES,
)

# Create the full prompt with few-shot examples included
full_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional resume optimizer that helps improve resumes for ATS systems."),
    few_shot_prompt,  # Include the few-shot examples as a message
    ("human", """
Below is a flawed or unstructured resume, a job description the candidate is applying to, and some helpful context from other successful resumes.

Use the job description and context to emphasize relevant skills and experiences. Your job is to rewrite and optimize the resume in valid JSON format aligned with ATS standards.

--- RAW RESUME ---
{raw_resume}

--- JOB DESCRIPTION ---
{job_description}

Please generate the optimized JSON resume:
""")
])

# Full chain with LLM and parser
resume_optimizer_chain = full_prompt | model | StrOutputParser()

# Invoke with real resume + JD
optimized_resume_json = resume_optimizer_chain.invoke({
    "raw_resume": raw_resume_text,
    "job_description": job_description
})

# Print or save the result
print(optimized_resume_json)

# Save to a file
with open("optimized_resume.json", "w") as f:
    f.write(optimized_resume_json)