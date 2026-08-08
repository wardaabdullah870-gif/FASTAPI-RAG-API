# FastAPI RAG Document Question Answering API

A Retrieval-Augmented Generation (RAG) application built with **FastAPI** that allows users to ask questions about their documents and receive answers based on the relevant document content.

The project uses document loading, text chunking, embeddings, vector search, and an LLM to build a complete RAG pipeline.

## Features

- FastAPI REST API
- PDF and text document processing
- Document chunking
- Text embeddings
- ChromaDB vector database
- Similarity-based document retrieval
- Retrieval-Augmented Generation (RAG)
- Question answering over documents
- Streamlit interface for testing
- Modular Python project structure
- Interactive FastAPI Swagger documentation

## How the RAG Pipeline Works

```text
PDF / Text Documents
        ↓
Document Loader
        ↓
Text Chunking
        ↓
Embeddings
        ↓
ChromaDB Vector Store
        ↓
Similarity Search
        ↓
Relevant Document Chunks

        ↓
LLM


Project Structure
FastAPI RAG Document Q&A
│
├── FastAPI API
│   └── /ask endpoint
│
├── Streamlit UI
│
├── RAG Pipeline
│   ├── Document Loader
│   ├── Text Chunker
│   ├── Embedding Generator
│   ├── Vector Store
│   ├── Retriever
│   └── RAG / Answer Generation
│
├── ChromaDB
│
├── Configuration
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── .gitignore
│
├── Tests
│   └── test_rag.py
│
└── GitHub Repository


Technologies Used
Python
FastAPI
LangChain
ChromaDB
Streamlit
Groq
RAG
Vector Embeddings
        ↓
Generated Answer
