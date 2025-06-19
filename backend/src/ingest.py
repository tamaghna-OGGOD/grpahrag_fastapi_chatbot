from langchain_openai import OpenAI
from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
openai_key = os.getenv("OPENAI_API_KEY")

graph = Neo4jGraph(url=uri, username=user, password=password)

def load_and_split(path: str = "../../data/mcp_doc.pdf"):
    loader = PyPDFLoader(path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)

if __name__ == "__main__":
    chunks = load_and_split()
    llm = OpenAI(openai_api_key=openai_key, temperature=0)
    transformer = LLMGraphTransformer(llm=llm)
    graph_documents = transformer.convert_to_graph_documents(chunks)
    graph.add_graph_documents(graph_documents)
    print(f"Ingested {len(graph_documents)} graph documents with nodes and relationships.")
