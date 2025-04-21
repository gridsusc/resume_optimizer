from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
import json

with open("resume-prompt.json", "r") as f:
    resume_data = json.load(f)

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

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant designed to extract and improve resume data for the following fields only: basics.summary, work.highlights, skills.keywords, and projects.highlights"),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
chain = final_prompt | model

response = chain.invoke({"input": resume_data})
parsed = json.loads(response.content)
print(json.dumps(parsed, indent=2))