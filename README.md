---
title: ContextAI
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
app_file: app.main
pinned: false
---
# ContextAI

A **FastAPI-based RAG application** that lets users upload documents (PDF/TXT) and ask questions.  
Powered by **LangChain**, **ChromaDB**, and **LLMs** for context-aware answers.

## 🚀 Live Demo

[![Live Demo](https://img.shields.io/badge/Demo-Live-brightgreen?style=for-the-badge)](https://rag-frontend-1y5k.onrender.com)


## 📚 FastAPI RAG App with LangChain, ChromaDB & Authentication

This project is a Retrieval-Augmented Generation (RAG) web application built with FastAPI.
It allows users to:

- 🔑 Sign up / Sign in (JWT-based authentication)

- 📂 Upload PDF or text documents

- 🧠 Store document embeddings in ChromaDB (vector database)

- 💬 Ask questions about uploaded documents

- ⚡ Get context-aware answers powered by LangChain + LLMs (via OpenRouter
)

## 🚀 Features

- User authentication with access & refresh tokens

- Secure file uploads (.pdf, .txt)

- Automatic text chunking & embedding with HuggingFace models

- Persistent vector store using ChromaDB

- RAG pipeline with LangChain’s RetrievalQA

- OpenRouter integration for running LLM queries

- CORS configured for frontend integration

## 🛠️ Tech Stack

- FastAPI

- LangChain

- ChromaDB

- SQLModel
  -  for user database

- HuggingFace Embeddings

- OpenRouter
  -  (for LLM access)

## 📂 Project Structure
`````
app/
 ├── main.py          # FastAPI routes & entrypoint
 ├── rag.py           # RAG pipeline (embeddings, vector store, QA chain)
 ├── models.py        # User models & schemas
 ├── auth.py          # Auth logic (hashing, tokens, verification)
 ├── database.py      # SQLModel setup
 └── config.py        # Settings & constants
uploads/              # User uploaded files (ignored in Git)
chroma_db/            # Vector DB storage (ignored in Git)
`````

## ⚙️ Setup & Installation
1️⃣ Clone the repo
  - git clone https://github.com/your-username/fastapi-rag-app.git
  - cd fastapi-rag-app

2️⃣ Create & activate virtual environment
  - python -m venv venv
  - source venv/bin/activate   # Linux/Mac
  - venv\Scripts\activate      # Windows

3️⃣ Install dependencies
  - pip install -r requirements.txt

4️⃣ Configure environment variables

  - Create a .env file in the project root (or copy from .env.example):

  - ### OpenRouter
  - OPENROUTER=your_openrouter_api_key_here

  - ### JWT secret
  - SECRET_KEY=your_super_secret_key

⚠️ Never commit your real .env file.

▶️ Run the App

  - Start the FastAPI server:

  - uvicorn app.main:app --reload


  - The API will be available at:
    - 👉 http://127.0.0.1:8000


## 🔑 Authentication Flow

  - Signup → POST /signup with username & password

  - Signin → POST /signin to receive access_token & refresh_token

  - Use Authorization: Bearer <access_token> for protected endpoints

## 📂 Document Workflow

- User logs in

- Upload document → POST /upload (PDF or TXT)

- Ask a question → GET /ask?q=your+question

- The system searches your embeddings in ChromaDB and queries the LLM with context

## 📝 Notes

- uploads/ and chroma_db/ are auto-created at runtime if they don’t exist.

- Both folders are ignored by Git (runtime data only).

- Contributions & pull requests are welcome 🚀