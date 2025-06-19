
# Rag FastAPI Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that ingests a PDF into a Neo4j knowledge graph and serves a Graph-Cypher QA API, with a simple Express/JavaScript frontend.

## Project Structure

```

rag\_fastapi\_chatbot/
├── backend/
│   ├── ingest.py          # Ingests PDF, builds nodes & relationships via LLMGraphTransformer
│   ├── main.py            # FastAPI app exposing `/chat` endpoint using GraphCypherQA
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Neo4j & OpenAI credentials
├── data/
│   └── sample\_document.pdf  # Place your source PDF here
└── frontend/
├── package.json       # npm metadata & start script
├── server.js          # Express server to serve `public/`
└── public/
└── index.html     # Chat UI: textarea → POST → `/chat`

````

## Prerequisites

- **Python 3.8+**  
- **Node.js 14+ & npm**  
- A **Neo4j** instance (local or cloud)  
- An **OpenAI** API key  

## Backend Setup

1. **Create & activate a virtual environment**  
   ```bash
   cd rag_fastapi_chatbot/backend
   python -m venv .venv
   source .venv/bin/activate        # macOS/Linux
   .\.venv\Scripts\Activate         # Windows PowerShell
````

2. **Install Python dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   In `backend/.env`, set:

   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=<your_password>
   OPENAI_API_KEY=<your_openai_key>
   ```

4. **Place your PDF**
   Copy your PDF into `backend/../data/sample_document.pdf`.

5. **Ingest the PDF into Neo4j**
   This will split the PDF into chunks, infer nodes & edges, and populate your graph:

   ```bash
   python ingest.py
   ```

6. **Run the FastAPI server**

   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   The Graph-RAG API will be live at `http://127.0.0.1:8000`.

## Frontend Setup

1. **Install dependencies**

   ```bash
   cd rag_fastapi_chatbot/frontend
   npm install
   ```

2. **Configure CORS proxy (optional)**
   If you encounter CORS issues, add to `package.json`:

   ```json
   "proxy": "http://localhost:8000"
   ```

3. **Start the Express server**

   ```bash
   npm start
   ```

   Your chat UI will be available at `http://localhost:3000` (or another port if configured).

## Usage

1. Open your browser to the frontend URL (e.g. `http://localhost:3000`).
2. Type a question in the textarea, e.g. “Summarize the document.”
3. Click **Send**—the frontend will POST to `/chat` and display the LLM’s answer.

## File Descriptions

* **backend/ingest.py**

  * Uses `PyPDFLoader` → splits via `RecursiveCharacterTextSplitter`
  * `LLMGraphTransformer` → `convert_to_graph_documents` + `ingest_graph_documents`

* **backend/main.py**

  * FastAPI app with CORS middleware
  * `/chat` endpoint powered by `GraphCypherQA`

* **frontend/server.js**

  * Serves `public/index.html` on port 3000 via Express

* **frontend/public/index.html**

  * Simple HTML/JS UI that fetches `POST http://localhost:8000/chat`



