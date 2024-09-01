import streamlit as st
import warnings
import json
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from streamlit_chat import message

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

def initialize_vector_db():
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name) 

    if os.path.exists("Database"):
        vectordb__=FAISS.load_local("Database", embeddings, allow_dangerous_deserialization=True)
        retriever__=vectordb__.as_retriever()
        return retriever__
    else:
        vectordb__=FAISS.from_documents(documents, embeddings)
        vectordb__.save_local("Database")
        retriever__=vectordb__.as_retriever()
        return retriever__

def create_retrieval_chain_from_db(db):
    # Set up the prompt
    prompt = ChatPromptTemplate.from_template("""
        Suppose you are an assistant to me (Diva). When people ask you about me, refer to the vector database(While searching from the database, try to fetch all the possible responses and club them and remove repetition) and tell them about me and my achievements.
        Reply in 3rd person's voice, for example if someone asks- tell me about diva. so tell them like you are telling about your creator, like diva is my creator and she has such such achievements and so on.
        
        <context>
        {context}
        </context>
        Question: {input}""")

    # Retrieve the model API key from environment variable
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


    # Initialize the LLaMA model
    model = ChatGroq(model="llama3-8b-8192")

    # Create the document chain
    document_chain = create_stuff_documents_chain(model, prompt)

    # Create the retrieval chain
    retrieval_chain = create_retrieval_chain(db, document_chain)

    return retrieval_chain

# Streamlit UI  
st.title("Diva's Assistant")

# Load data and initialize the retrieval chain
try:
    file_path = 'data.json'
    data = load_data(file_path)
    documents = create_documents(data)
    vectordb = initialize_vector_db()
    retrieval_chain = create_retrieval_chain_from_db(vectordb)
except Exception as e:
    st.error(f"An error occurred: {e}")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input and response display
user_input = st.text_input("Ask me anything about Diva!", "")

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

count = 0
# Display chat messages
for chat in st.session_state['chat_history']:
    if chat["role"] == "user":
        message(chat["content"], is_user=True, key=count)
    else:
        message(chat["content"], is_user=False, key=count)
    count += 1

# Adding a send button for a better UI experience
st.button("Send")

