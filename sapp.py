import streamlit as st
import warnings
import json
from pathlib import Path
from langchain.docstore.document import Document
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.embeddings import OllamaEmbeddings
from streamlit_chat import message  # Streamlit Chat library for chat UI

# Suppress warnings
warnings.filterwarnings("ignore")

# Load and process data
@st.cache_data
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_documents(data):
    documents = []
    for key, value in enumerate(data['data']):
        page_content = json.dumps({key: value})
        documents.append(Document(page_content=page_content, metadata={}))
    return documents

def initialize_vector_db(documents):
    embeddings = OllamaEmbeddings()
    return FAISS.from_documents(documents,embeddings)

def create_retrieval_chain_from_db(db):
    llm = Ollama(model="llama3")  # Use LLaMA 3 model
    prompt = ChatPromptTemplate.from_template("""
        Suppose you are an assistant to me (Diva). When people ask you about me, refer to the database and tell them about me. You can use the tag as the keywords. If the question asked to you and any word in that question matches or semantically is similar to the tag, consider the patterns as questions and fetch those particular responses and use these question answers as a prototype to answer the question asked to you.
        Reply in a formal tone, avoiding sarcasm, and focus on accuracy. Keep sentences short and fact-based.

        <context>
        {context}
        </context>
        Question: {input}""")
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = db.as_retriever()
    return create_retrieval_chain(retriever, document_chain)

# Streamlit UI  
st.title("Diva's Assistant")

# Load data and initialize the retrieval chain
try:
    file_path = 'data.json'
    data = load_data(file_path)
    documents = create_documents(data)
    vectordb = initialize_vector_db(documents)
    retrieval_chain = create_retrieval_chain_from_db(vectordb)
except Exception as e:
    st.error(f"An error occurred: {e}")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input and response display
user_input = st.text_input("So tell me a bit about Diva's Skillset.", "")

if user_input:
    # Add user input to chat history
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    
    try:
        # Get assistant response
        response = retrieval_chain.invoke({"input": user_input})
        assistant_response = response['answer']

        # Add assistant response to chat history
        st.session_state['chat_history'].append({"role": "assistant", "content": assistant_response})
    
    except Exception as e:
        assistant_response = f"An error occurred while processing your request: {e}"
        st.session_state['chat_history'].append({"role": "assistant", "content": assistant_response})

# Display chat messages
for chat in st.session_state['chat_history']:
    if chat["role"] == "user":
        message(chat["content"], is_user=True)
    else:
        message(chat["content"], is_user=False)

# Adding a send button for a better UI experience
st.button("Send")
