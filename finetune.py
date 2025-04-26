import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

# Load resume (str)
def load_raw_resume(path: str) -> str:
    with open(path, 'r') as file:
        json_prompt = json.load(file)
    # Escape curly braces for template formatting
    return json.dumps(json_prompt, indent=2).replace("{", "{{").replace("}", "}}")

# few shot prompting using exmamples retrieved
def create_few_shot_prompt(examples):
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}")
    ])
    return FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )


# write the full prompt and chain

def build_resume_optimizer_chain(few_shot_prompt):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a professional resume optimizer that helps improve resumes for ATS systems."),
        few_shot_prompt,
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

    model = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.1,
    )

    return prompt_template | model | StrOutputParser()


def optimize_resume(raw_resume_path: str, related_templates, job_description: str, output_path: str):
    raw_resume_text = load_raw_resume(raw_resume_path)
    few_shot_prompt = create_few_shot_prompt(related_templates)
    optimizer_chain = build_resume_optimizer_chain(few_shot_prompt)

    result = optimizer_chain.invoke({
        "raw_resume": raw_resume_text,
        "job_description": job_description
    })

    with open(output_path, "w") as f:
        f.write(result)

