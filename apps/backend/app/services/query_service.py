import requests
from sentence_transformers import util
from app.utils.text_processing import model
from app import config

def search_best_document(query, documents, embeddings):
    query_embedding = model.encode(query, convert_to_tensor=True)
    best_doc, best_score = {}, float('-inf')

    for doc in documents:
        score = util.cos_sim(query_embedding, embeddings[doc["id"]]).item()
        if score > best_score:
            best_score = score
            best_doc = doc
    return best_doc if best_doc else None

def call_groq(messages, temperature=0.2):
    payload = {
        "model": config.GROQ_MODEL,
        "messages": messages,
        "temperature": temperature
    }
    response = requests.post(config.GROQ_URL, headers=config.GROQ_HEADERS, json=payload)
    return response.json()

def call_openai(messages, model="gpt-4o-mini", temperature=0.4):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    response = requests.post(config.OPENAI_URL, headers=config.OPENAI_HEADERS, json=payload)
    return response.json()

