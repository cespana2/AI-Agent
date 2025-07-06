# 🧠 AI Agent Document QA

This full-stack project enables semantic question-answering over PDF and DOCX documents. It uses **FastAPI** as the backend to handle document parsing, embedding, search, and answer generation, and a **React** frontend to upload documents and ask natural language questions.

---

## 🚀 Features

- Upload PDF or DOCX documents
- Convert documents to Markdown and HTML tables
- Chunk and embed content using SentenceTransformers
- Store chunks in a FAISS index and a relational DB
- Perform semantic search and generate answers using an LLM
- Clean, modern frontend built with React

---

## 🛠️ Tech Stack

### Backend

- **FastAPI** for REST API
- **SentenceTransformers** for embeddings
- **FAISS** for vector similarity search
- **SQLAlchemy** + SQLite (or any DB)
- **pymupdf4llm** and **mammoth** for PDF/DOCX parsing
- **OpenAI** (optional) for answer generation

### Frontend

- **React** with functional components
- **Axios** for API requests
- **CRA** for development

---

## 📦 Project Structure
├── backend/
│   ├── main.py
│   ├── prompts/
│   ├── models/
│   ├── utils/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── index.js
│   └── .env
└── README.md

---

## ⚙️ Setup Instructions

### Clone the Repo

```bash
git clone https://github.com/cespana2/AI-Agent.git
cd AI Agent
```

## ⚙️ Backend Setup (FastAPI)

### 1. Go to the backend folder

### 2. Create a .env file

```bash
DATABASE_URL=sqlite:///./db.sqlite3
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
GEN_MODEL_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-...
```

### 3. Install Dependencies and Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```

## ⚙️ Frontent Setup (React)

### 1. Go to Frontend Folder

```bash
cd frontend
```

### 2. Create a .env file

```bash
REACT_APP_API_URL=http://localhost:3000
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Run the app

```bash
npm start      # For Create React App
```

📍 Frontend will run at: http://localhost:3000

## 🔄 Local Development Notes
	•	CORS is enabled on the backend to allow requests from localhost:3000
	•	Ensure both frontend and backend .env files are set correctly
	•	Upload requests should be sent as multipart/form-data


The API will be available at:
📍 http://localhost:8000

---

### 🧪 API Endpoints

## POST /upload/

Upload a PDF or DOCX file. Automatically chunks and indexes its content.

Request:
	•	multipart/form-data with file=<yourfile>

Response:
```json
{
  "message": "Uploaded and indexed.",
  "chunks": 5,
  "ids": ["..."]
}
```

## GET /answer/?query=...

Semantic search + LLM response for a user question.

Example:
GET /answer/?query=What is the carbon offset in 2023?

## GET /debug/chunks

Returns all indexed document chunks (from DB).

---

### 🧠 Customizing

## Change the Embedding Model

Update EMBEDDING_MODEL in .env (e.g., try all-MiniLM-L6-v2).

## Use Another LLM

Customize generate_answer() in utils/prompt_utils.py.
