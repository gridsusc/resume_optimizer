# Import required libraries with updated imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import json, re, torch
import os # hardcode in the portal: export HF_TOKEN=your_HF_token_here


# ======== Config ========
model_id = "meta-llama/Llama-3.2-1B-Instruct"
cache_dir = "./hf_models"
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

# ======== Model Setup ========
print("Loading model...")
token = os.environ.get("HF_TOKEN")

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    cache_dir=cache_dir,
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device in ["mps", "cuda"] else torch.float32,
    cache_dir=cache_dir,
)
print("Model loaded.")


# You can change this
text_generation_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.1,
    top_p=0.9,
    repetition_penalty=1.1,
)

 
llm = HuggingFacePipeline(
    pipeline=text_generation_pipeline,
    model_kwargs={"return_full_text": False}
)

# ======== Load Input ========
with open("resume.json", "r") as f:
    resume_data = json.load(f)

with open("jd.txt", "r") as f:
    job_description = f.read()

# Prompt instruction
human_prompt = """
[Job Description]
\"\"\"{job_description}\"\"\"

[Resume Data]
\"\"\"{resume_data}\"\"\"

You are a helpful AI assistant designed to verify and correct basics (summary), work, education, skills, projects parts in resumes.
Don't change other parts that I didn't mention above.

Follow this procedure when you check: 

1. For education:
Your responsibilities include checking for typos, verifying university existence,
and ensuring a logically consistent timeline for degrees (e.g., Bachelor's before Master's).
Make sure that there are no overlapping periods, and that multiple Bachelor's or Master's degrees are allowed.
Check that courses align with the declared major, and delete the course number (e.g. DB1101) if it exists.
Do not alter any other thing.

2. For basic:
You only check the summary, make it more fluent and close to job description based on what exists in the resume, 
and do not create new things. 

3. For skills: 
Just check typo and verifying skill existence.

4. For projects:
Make the description more close to the given job description.

5. For all the things you change, make sure you put them into the corresponding highlight part. 

Return ONLY a valid JSON object, with no extra text or explanation.
"""

prompt_template = ChatPromptTemplate.from_template(human_prompt)
output_parser = StrOutputParser()
resume_chain = prompt_template | llm | output_parser

# ======= Invoke ========
print("Invoking the chain...")
try:
    response = resume_chain.invoke(
        {"resume_data": json.dumps(resume_data, indent=2),
        "job_description": job_description
    })
    print("Chain invoked successfully")
    try:
        # Extract JSON substring (starting with `{` and ending with `}`)
        json_start = response.find("{")
        json_str = response[json_start:].strip()

        # Optional: regex to ensure outer JSON object
        match = re.search(r"\{.*\}", json_str, re.DOTALL)
        if match:
            json_str = match.group(0)

        parsed_output = json.loads(json_str)

        # Pretty-print
        print(json.dumps(parsed_output, indent=2))

        # Save
        with open("output_parsed.json", "w") as f:
            json.dump(parsed_output, f, indent=2)
    except json.JSONDecodeError:
        print("GPT returned non-parseable JSON:")
        print(response)

except Exception as e:
    print(f"Error invoking chain: {e}")
