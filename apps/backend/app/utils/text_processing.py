import os
import re
import pickle
import nltk
from sentence_transformers import SentenceTransformer
from .file_loaders import extract_text_from_pdf, ppt_to_text
from app import config
from nltk.tokenize import sent_tokenize

# Baixa o tokenizador de sentenças do NLTK (apenas 1x)
nltk.download("punkt", quiet=True)


# modelo anterios: all-MiniLM-L6-v2
# Modelo de melhor qualidade e suporte multi-idioma
model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")



def clean_text(text: str) -> str:
    #Remove espaços extras e normaliza o texto.
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text: str, chunk_size: int):
    #Divide o texto em chunks completos, sem cortar frases pela metade.
    sentences = sent_tokenize(text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) <= chunk_size:
            current += " " + sentence
        else:
            chunks.append(current.strip())
            current = sentence
    if current:
        chunks.append(current.strip())

    return chunks

def load_or_create_embeddings(file_path: str, cache_path: str, source_type: str):
    #Carrega embeddings do cache ou cria novos se não existirem.
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Extração do texto
    if source_type == "pdf":
        text = extract_text_from_pdf(file_path)
    elif source_type == "pptx":
        text = ppt_to_text(file_path)
    else:
        raise ValueError("Tipo de arquivo inválido")

    # Limpeza e chunking
    text = clean_text(text)
    chunks = chunk_text(text, config.CHUNK_SIZE)

    documents = [
        {"id": f"{source_type}_{i}", "text": chunk}
        for i, chunk in enumerate(chunks)
    ]

    # Geração dos embeddings com normalização
    doc_embeddings = {
        doc["id"]: model.encode(
            doc["text"],
            convert_to_tensor=True,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=True
        )
        for doc in documents
    }

    # Cache para evitar processamento repetido
    with open(cache_path, "wb") as f:
        pickle.dump((documents, doc_embeddings), f)

    return documents, doc_embeddings
