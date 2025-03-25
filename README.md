# Chat with PDF using RAG

## Overview
This project enables users to interact with PDF documents using AI-powered conversational capabilities. By leveraging a Retrieval-Augmented Generation (RAG) system, it extracts information from PDFs to provide accurate and contextual responses. It's an ideal solution for users seeking insights from large PDF documents without manually reading through them.

## Features
- Upload PDF files for analysis
- Perform natural language queries on PDF content
- AI-powered conversational responses using RAG
- Fast and scalable API using FastAPI
- Seamless database management with SQLite3 for PDF details and Chroma DB for embeddings
- Support for large documents and complex queries

## Infrastructure Workflow
1. **PDF Upload**: The PDF document is uploaded using the API endpoint.
2. **Preprocessing**: The content is extracted using PyPDF.
3. **Storage**: Basic PDF details are stored in an SQLite3 database, and embeddings are generated and stored using Chroma DB.
4. **AI Processing**: Using LangChain and Ollama embeddings, the RAG model generates responses.
5. **Response Generation**: The result is returned as a conversational AI response.

## Technologies Used
- FastAPI
- LangChain
- OpenAI
- PyPDF
- Ollama Embeddings
- Ollama LLM
- SQLite3
- Chroma DB

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/abhishekpatra8/chat_with_PDF_RAG
    cd chat_with_PDF_RAG
    ```

2. Create and activate a virtual environment:
## Using Python Virtual Environment
    ```bash
    python3.11 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

## Using Conda
    ```bash
    conda create -n chat_with_pdf_rag python=3.11
    conda activate chat_with_pdf_rag
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your `.env` file with the necessary environment variables, including your OpenAI API key and database connection.

## Usage

1. Start the FastAPI server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

2. Access the API documentation:
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

3. Upload a PDF and start asking questions using the API endpoints.

## Folder Structure
```plaintext
chat_with_PDF_RAG
├── apis
│   ├── chat_with_doc.py
│   ├── file_ops.py
├── db
│   ├── database.py
│   ├── pdf_records.db
├── models
│   ├── model.py
├── tests
│   ├── test_main.py
├── main.py
├── requirements.txt
└── .env
```

## RAG Flow Diagram
![alt text](rag_flow.png)