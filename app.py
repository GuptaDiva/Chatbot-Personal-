from flask import Flask, request, jsonify, render_template
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
import os

STATIC_DIR = os.path.abspath('./static')
app = Flask(__name__, static_folder=STATIC_DIR)

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
       You are an AI assistant representing Diva. Your task is to provide accurate and formal responses when people ask about Diva, her achievements, or related information. Always refer strictly to the information available in the provided context from the vector database.

        When responding:
        - Use a formal tone, keeping your answers respectful and professional.
        - Provide concise, fact-based responses, avoiding unnecessary elaboration.
        - Ensure all information is accurate and relevant to the query.
        - Avoid sarcasm, humor, or speculative answers. Stick to the facts presented in the context.
        - If you are unsure about any detail, indicate that the information is not available rather than guessing.

        Example scenario: If someone asks, "Tell me about Diva," respond as follows: "Diva is the creator of this assistant. She has achieved [specific achievements from the database]."

        <context>
        {context}
        </context>
        Question: {input}
                        """)
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = db.as_retriever()
    return create_retrieval_chain(retriever, document_chain)

def get_chatbot_response(user_input):
    """Process user input and return chatbot response."""
    file_path = 'data.json'
    data = load_data(file_path)
    documents = create_documents(data)
    vectordb = initialize_vector_db(documents)
    retrieval_chain = create_retrieval_chain_from_db(vectordb)
    response = retrieval_chain.invoke({"input": user_input})
    return response['answer']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = get_chatbot_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
    