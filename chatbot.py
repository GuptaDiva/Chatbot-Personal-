import warnings
warnings.filterwarnings("ignore")
import json
from pathlib import Path
from langchain.docstore.document import Document
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.embeddings import OllamaEmbeddings

def load_data(file_path):
    """Load and return data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def create_documents(data):
    """Convert data into a list of Document objects."""
    documents = []
    for key, value in enumerate(data['data']):
        page_content = json.dumps({key: value})
        documents.append(Document(page_content=page_content, metadata={}))
    return documents

def initialize_vector_db(documents):
    """Initialize and return a Chroma vector database with Ollama embeddings."""
    embeddings = OllamaEmbeddings()
    return Chroma.from_documents(documents, embeddings)

def create_retrieval_chain_from_db(db):
    """Create and return a retrieval chain."""
    llm = Ollama(model="llama2")
    prompt = ChatPromptTemplate.from_template("""
        Suppose you are an assistant to me (Diva). When people ask you about me, refer to the vector database and tell them about me and my achievements.
        Reply in 3rd person's voice, for example if someone asks- tell me about diva. so tell them like you are telling about your creator, like diva is my creator and she has such such achievements and so on.

        <context>
        {context}
        </context>
        Question: {input}""")
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = db.as_retriever()
    return create_retrieval_chain(retriever, document_chain)

def main():
    file_path = 'data.json'
    
    # Load and process data
    try:
        data = load_data(file_path)
        documents = create_documents(data)
    
        # Initialize vector database
        vectordb = initialize_vector_db(documents)
    
        # Create retrieval chain
        retrieval_chain = create_retrieval_chain_from_db(vectordb)
    
        # Example query
        response = retrieval_chain.invoke({"input": "Who is Diva?"})
        print(response['answer'])
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
