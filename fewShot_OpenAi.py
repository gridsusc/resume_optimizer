from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
import json

with open("resume-prompt.json", "r") as f:
    resume_data = json.load(f)

with open("jd.txt", "r") as f:
    job_description = f.read()

examples = [
    {
        "input": """{
            "work": [
            {
                "highlights": [
                    "Worked on this project at my internship where we had to clean a ton of messy sales data — I wrote a few scripts in Python to fix formatting and missing stuff",
                    "I also helped make some visuals in Tableau to show trends to the marketing team",
                    "At one point, we had a bug that was breaking everything — I figured out it was due to mismatched date formats"
                ]
            }
            ]
        }""",
        "output": """{
            "work": [
            {
                "highlights": [
                    "Developed Python scripts for data cleaning and transformation, reducing manual data wrangling time by 40%",
                    "Created interactive Tableau dashboards to visualize sales trends and support marketing decision-making",
                    "Identified and resolved critical data pipeline issue related to inconsistent date formats, ensuring report accuracy"
                ]
            }
            ]
        }""",
    },
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

system_prompt = """
You are a helpful AI assistant designed to extract and improve resume data for the following fields only: "basics.summary", "work.highlights", "skills.keywords", and "projects.highlights".

Use only the information in the candidate's resume.
1. For basic:
You only check the summary, make it more fluent and close to job description based on what exists in the resume, 
and do not create new things. 

2. For skills: 
Just check typo and verifying skill existence.

3. For projects:
Make the description more close to the given job description.

4. For all the things you change, make sure you put them into the corresponding highlight part.
"""

final_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    few_shot_prompt,
    ("human", "Resume JSON:\n{resume}\n\nJob Description:\n{jd}"),
])


model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
chain = final_prompt | model

response = chain.invoke({
    "resume": json.dumps(resume_data),
    "jd": job_description
})
parsed = json.loads(response.content)
print(json.dumps(parsed, indent=2))

with open("resume-improved.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)