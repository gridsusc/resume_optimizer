
import pdfplumber
from langchain_community.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from resume_schema import Resume
import os

def convert_pdf_to_json(pdf_filepath: str, openai_key: str) -> dict:
    pdf_text = ''
    with pdfplumber.open(pdf_filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text += page_text + '\n'

    os.environ["OPENAI_API_KEY"] = openai_key
    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    parser = PydanticOutputParser(pydantic_object=Resume)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a resume parser. Extract the resume information from the text into structured JSON format."),
        ("human", "{text}\n\n{format_instructions}")
    ])

    chain = (
        {
            "text": RunnablePassthrough(),
            "format_instructions": RunnablePassthrough()  # dynamically inject parser format
        }
        | prompt
        | llm
        | parser
    )

    resume_obj = chain.invoke({
        "text": pdf_text,
        "format_instructions": parser.get_format_instructions()
    })

    return resume_obj.dict()


if __name__ == '__main__':
    from getpass import getpass
    openai_key = getpass("OpenAI Key: ")
    pdf_path = 'data/Richard Hendriks.pdf'

    resume_json = convert_pdf_to_json(pdf_path, openai_key)
    print(json.dumps(resume_json, indent=2))
