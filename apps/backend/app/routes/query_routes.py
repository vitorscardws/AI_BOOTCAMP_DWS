from fastapi import APIRouter, HTTPException
from app.models import QueryRequest
from app.utils.text_processing import load_or_create_embeddings
from app import config
from app.services import query_service

router = APIRouter()

pdf_docs, pdf_embeddings = load_or_create_embeddings(config.PDF_PATH, config.CACHE_PATH_PDF, "pdf")
ppt_docs, ppt_embeddings = load_or_create_embeddings(config.PPTX_PATH, config.CACHE_PATH_PPTX, "pptx")

@router.post("/query")
async def query(request: QueryRequest):
    best_doc = query_service.search_best_document(request.query, pdf_docs, pdf_embeddings)
    if not best_doc:
        raise HTTPException(status_code=404, detail="No relevant document found.")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Magic: The Gathering expert helping new players. "
                "Answer using only the provided content, but never mention or hint at the source or the text. "
                "Preserve the language of the user's question (if the question is in Portuguese, respond in Portuguese). "
                "Use a clear, friendly, and conversational tone. "
                "Be concise and objective, focusing only on what was asked. "
                "Do not guess or add information not found in the content."
                "**Format your answer using Markdown**. "
                "Use tables, bold, italics, and lists whenever appropriate and format the paragraphs and spaces."
            )
        },
        {
            "role": "user",
            "content": f"""
            {best_doc['text']}

            Question:
            {request.query}
            """
        }
    ]

    try:
        response = query_service.call_groq(messages)
        return {"response": response["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/ppt-search")
async def query_pptx(request: QueryRequest):
    best_doc = query_service.search_best_document(request.query, ppt_docs, ppt_embeddings)
    if not best_doc:
        raise HTTPException(status_code=404, detail="No relevant document found.")
    
    print(f"Best document: {best_doc['text']}")  # Debugging line to see the best document

    messages = [
        {
            "role": "system",
            "content": (
                "Always respond in the exact same language as the user's question, preserving tone and style. "
                "If the question is in Portuguese, answer in Portuguese; if in English, answer in English; if in another language, answer in that language. "
                "You are an expert communicator who summarizes and explains the content of a PowerPoint presentation "
                "in a clear, engaging, and easy-to-understand way. "
                "Use only the information provided in the document text — do not guess or add information that is not present. "
                "Rewrite bullet points or fragmented text into complete, well-structured sentences. "
                "Do not mention slides, bullet points, or that this came from a presentation. "
                "If the answer is not found in the text, say so clearly. "
                "**Format your answer using Markdown**. "
                "Use tables, bold, italics, and lists whenever appropriate. "
                "When creating hierarchical lists, indent subitems with exactly two spaces. "
                "Always leave one blank line after a title before starting a list. "
                "Never mix a title and a list on the same line. "
                "Example of correct Markdown list formatting:\n"
                "## Título Principal\n"
                "- Item 1\n"
                "  - Subitem 1.1\n"
                "  - Subitem 1.2\n"
                "- Item 2\n"
                "  - Subitem 2.1\n"
                "  - Subitem 2.2\n"
            )
        },
        {
            "role": "user",
            "content": f"""
            {best_doc['text']}

            Question:
            {request.query}
            """
        }
    ]

    try:
        response = query_service.call_openai(messages, model="gpt-4o-mini", temperature=0.4)
        # response = query_service.call_groq(messages)
        return {"response": response["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/text-to-mongo")
async def text_to_mongo(request: QueryRequest):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a MongoDB expert. Your task is to convert natural language requests into valid MongoDB queries in JSON format.\n"
                "You MUST follow these strict rules:\n"
                "1. Only return the query, no explanations or markdown.\n"
                "2. You can interpret common business, financial, or database-related terminology, including date filters and numeric comparisons.\n"
                "3. NEVER assume field names — only use field names that are directly mentioned or clearly implied by the request.\n"
                "4. If you cannot confidently generate a valid query, respond with exactly:\n"
                '"Unable to generate a valid MongoDB query from the input."'
            )
        },
        {
            "role": "user",
            "content": (
                f'Convert the following request into a valid MongoDB query. '
                f'Input: "{request.query}"\n\n'
                "Answer:"
            )
        }
    ]

    try:
        # response = query_service.call_groq(messages)
        response = query_service.call_openai(messages, model="gpt-3.5-turbo", temperature=0.0)
        mongo_query = response['choices'][0]['message']['content'].strip()
        return {"response": mongo_query}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
