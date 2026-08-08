import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.loader import DocumentLoader
from app.chunker import TextChunker
from app.embedder import EmbeddingManager
from app.vector_store import VectorStore
from app.rag import RAGPipeline

app = FastAPI()


# Upload directory
UPLOAD_DIR = Path("app/data/documents/pdf_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Initialize RAG components
document_loader = DocumentLoader()
chunker = TextChunker()
embedding_manager = EmbeddingManager()
vector_store = VectorStore()

rag_pipeline = RAGPipeline(
    vector_store=vector_store,
    embedding_manager=embedding_manager
)


@app.get("/")
def home():
    return {"message": "RAG API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # 1. Save uploaded PDF
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 2. Load the uploaded PDF
    documents = document_loader.load_single_pdf(
        str(file_path)
    )

    # 3. Split documents into chunks
    chunks = chunker.split_documents(documents)

    # 4. Extract text from chunks
    texts = [
        doc.page_content
        for doc in chunks
    ]

    # 5. Generate embeddings
    embeddings = embedding_manager.generate_embeddings(
        texts
    )

    # 6. Store chunks and embeddings in ChromaDB
    vector_store.add_documents(
        documents=chunks,
        embeddings=embeddings
    )

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    }

class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    result = rag_pipeline.answer_question(
        question=request.question
    )

    return result