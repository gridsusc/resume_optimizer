import json
from typing import List, Dict
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

def get_data_science_templates(templates_list: List[Dict]) -> List[Dict]:
    documents = [
        Document(
            page_content=json.dumps(item, indent=2) # Store the full object as JSON string
        )
        for item in templates_list
    ]

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    chroma_db = Chroma.from_documents(
        documents, # using the entire document 
        embedding_function
    )

    query_1 = "python data analysis visualization"
    query_2 = "nlp data analysis"

    results_1 = chroma_db.similarity_search(query_1, k=1)
    results_2 = chroma_db.similarity_search(query_2, k=1)

    results_1_json = json.loads(results_1[0].page_content)
    results_2_json = json.loads(results_2[0].page_content)

    results = [
        results_1_json,
        results_2_json
    ]

    return results

if __name__ == '__main__':

    from data.resume_templates import RESUME_TEMPLATES


    payload = get_data_science_templates(RESUME_TEMPLATES)
    print(json.dumps(payload, indent=2))
