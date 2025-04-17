# Import required libraries with updated imports
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import json

model_id = "meta-llama/Llama-3.2-3B-Instruct"
cache_dir = "./hf_models"

# Check device availability - this is for my macbook / you can use cuda if on windows
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

# Load tokenizer
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    cache_dir=cache_dir
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device in ["mps", "cuda"] else torch.float32,
    device_map="auto",
    cache_dir=cache_dir
)

text_generation_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    temperature=0.1,
    top_p=0.9,
    repetition_penalty=1,
    return_full_text=False,
    clean_up_tokenization_spaces=True
)

llm = HuggingFacePipeline(
    pipeline=text_generation_pipeline,
    model_kwargs={"return_full_text": False} # this line could be deleted
)


json_parser = JsonOutputParser()

targeted_resume_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert resume parser and JSON generator.
    Given a professional's experience description, generate a structured JSON representation
    of their work history. Focus only on the work experience section.

    Output Format Instructions:
    - Generate a JSON array of work experiences
    - Each work experience should include:
      * name: Company/Organization name
      * position: Job title
      * startDate: Start date in YYYY-MM-DD format
      * endDate: End date in YYYY-MM-DD format (use current date if still employed)
      * summary: Brief description of the role
      * highlights: Key achievements or responsibilities

    Ensure the JSON is valid and well-structured."""),

    ("user", "Extract work experience from the following description:\n{context}")
])

work_experience_chain = targeted_resume_prompt | llm | json_parser

input_text = """
John Smith worked at TechCorp as a Senior Software Engineer from 2018 to 2023.
During his tenure, he led the development of a cloud-native microservices platform,
reducing system latency by 40%. He implemented CI/CD pipelines and mentored junior
developers. Prior to TechCorp, he was a Software Engineer at InnovateNow from 2015
to 2018, where he developed machine learning algorithms for predictive analytics.
"""

work_experience = work_experience_chain.invoke({"context": input_text})

print(json.dumps(work_experience, indent=2))


