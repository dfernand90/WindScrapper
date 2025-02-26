from pathlib import Path
from llama_index.readers.file.html.base import HTMLTagReader
from llama_index.core.node_parser.relational.unstructured_element import UnstructuredElementNodeParser
from llama_index.core.schema import Document
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from image_and_table_retriever import extract_images_and_tables
import random
import string

def load_html_directory(directory_path: str, tag: str = "section", ignore_no_id: bool = False):
    """
    Loads and parses HTML files from a specified directory.
    
    Args:
        directory_path (str): Path to the directory containing HTML files.
        tag (str): HTML tag to extract content from (default is "section").
        ignore_no_id (bool): Whether to ignore elements without an ID (default is False).
    
    Returns:
        tuple: Two lists of parsed document nodes with and without raw HTML metadata.
    """
    html_reader = HTMLTagReader(tag=tag, ignore_no_id=ignore_no_id)
    node_parser = UnstructuredElementNodeParser()
    documents, documents_w = [], []
    
    directory = Path(directory_path)
    for html_file in directory.glob("*.html"):
        docs = html_reader.load_data(html_file)
        
        for doc in docs:
            document = Document(
                text=doc.text,
                metadata={"text": doc.text[:1022], "id": doc.node_id}
            )
            documents.extend(node_parser.get_nodes_from_documents([document]))
            
            document_w = Document(
                text=doc.text,
                metadata={"text": doc.text[:1022], "html": doc.metadata.get("html_content"), "id": doc.node_id}
            )
            documents_w.extend(node_parser.get_nodes_from_documents([document_w]))
            
    return documents, documents_w

def generate_random_id(length=10):
    # Define the characters to choose from (uppercase, lowercase, digits)
    characters = string.ascii_letters + string.digits
    # Randomly select characters and join them into a string
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

def llm_web_scraper(llm_name: str, html_path: str, html_assets: str, query: str):
    """
    Processes HTML documents, extracts text, and queries an LLM for insights.
    
    Args:
        llm_name (str): Name of the LLM model to use.
        html_path (str): Path to the HTML files directory.
        html_assets (str): Path to associated HTML assets (e.g., images, tables).
        query (str): Query to retrieve relevant information from the documents.
    
    Returns:
        None
    """
    # Configure LLM and embedding settings
    llm = Ollama(model=llm_name, temperature=0.5, request_timeout=60.0)
    Settings.chunk_size = 1028
    Settings.chunk_overlap = 50
    Settings.llm = llm
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # Load HTML documents
    documents, documents_w = load_html_directory(html_path, tag="section", ignore_no_id=False)
    
    # Create a vector index from documents and query the LLM
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    
    # Extract best-matching document chunk
    best_chunks = response.source_nodes
    if isinstance(best_chunks, list):
        best_chunk = best_chunks[0] 
    else: 
        best_chunks
    best_chunk_index = next((i for i, doc in enumerate(documents) if doc.metadata.get("text", "") == best_chunk.metadata.get("text", "")), -1)
    best_chunk_html = documents_w[best_chunk_index].metadata.get("html", "") if best_chunk_index != -1 else ""
    
    # Retrieve short paper name from LLM
    #response_name = query_engine.query("give me a short name for the paper like lastname and publication year, max 10 characters, no spaces")
    random_id = generate_random_id(10)

    # Extract images and tables from the best-matching HTML section
    extract_images_and_tables(str(response.response), best_chunk_html, html_directory=html_assets, paper_short_name=random_id)

def main():
    """
    Main execution function to run the web scraper.
    """
    html_path = "path to a paper"
    html_assets = "path to assest folder"
    query = "What are the force coefficients for this project?"
    
    llm_web_scraper("llama3:8b", html_path, html_assets, query)
    
if __name__ == "__main__":
    main()

