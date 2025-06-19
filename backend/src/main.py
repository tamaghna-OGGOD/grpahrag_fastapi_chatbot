from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging

from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain

# Setup logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
openai_key = os.getenv("OPENAI_API_KEY")
if not all([uri, user, password, openai_key]):
    raise ValueError("Missing env vars: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, OPENAI_API_KEY")

app = FastAPI(title="Graph-RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = Neo4jGraph(url=uri, username=user, password=password)
llm = ChatOpenAI(openai_api_key=openai_key, temperature=0)
qa_chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=False,  # Set to False for production
    allow_dangerous_requests=True
)

class Query(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

@app.post("/chat", response_model=Answer)
def chat(query: Query):
    if not query.question:
        raise HTTPException(status_code=400, detail="Question is required")
    try:
        result = qa_chain.invoke({"query": query.question})
        return Answer(answer=result["result"])
    except Exception as e:
        logging.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

