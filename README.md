# 💬 Diva's Assistant - AI Chatbot

This project implements an AI-powered chatbot using Flask for backend, alongside [Streamlit](https://streamlit.io/), [LangChain](https://www.langchain.com/), and the LLaMA model via [Groq](https://groq.com/). The chatbot interacts through a web interface and answers questions about the creator (Diva Gupta) by providing personalized responses, leveraging a vector database for accurate information retrieval.

## 🛠️ Features
- **Conversational AI:** Utilizes the `llama3-8b-8192` model from Groq to generate responses.
- **Custom Retrieval:** Queries a vector database containing information about Diva, delivering tailored responses about her achievements.
- **Flask Backend:** The chatbot is supported by a Flask server that renders the main HTML interface.
- **Interactive UI:** Styled with CSS and JS (as shown in `static/chatbot.css` and `chatbot.js`) for smooth user interaction.
- **Chat History:** Displays chat history for users to review past queries and responses.

## 🚀 Live Demo

You can see the live demo of this project on Streamlit- [AI Assitant](https://diva-assistant.streamlit.app/)

## 🚀 Deployment

This project uses Flask for backend routing and Streamlit for chatbot interaction. Follow the steps below to set it up locally.

### 1. Clone the Repository

```bash
git clone https://github.com/GuptaDiva/Chatbot-Personal-.git
cd Chatbot-Personal-
```

### 2. Install Dependencies

Ensure all required dependencies are installed using the `requirements.txt`.

```bash
pip install -r requirements.txt
```

The key dependencies include:
- Flask
- Streamlit
- LangChain
- FAISS (for vector database)
- Ollama Groq (for model API)

### 3. Run Flask Server

The Flask app manages the backend logic. Start the server using the following command:

```bash
python app.py
```

### 4. Run the Chatbot

Once the Flask server is running, use Streamlit to interact with the chatbot UI. Open another terminal window and run:

```bash
streamlit run application.py
```

Open your web browser and navigate to the Flask endpoint (e.g., `http://localhost:5000`) or the Streamlit interface provided in the terminal (e.g., `http://localhost:8501`).

## 📂 Project Structure

```
📦divas-assistant-chatbot
 ┣ 📂Database               # Folder for database or model files
 ┣ 📂static                 # Contains CSS, JS, and image assets
 ┃ ┣ 📜chatbot.css          # Styles for chatbot UI
 ┃ ┣ 📜chatbot.js           # JavaScript for UI functionality
 ┃ ┗ 📜photo.jpg            # Image used in the project
 ┣ 📂templates              # HTML templates for Flask routes
 ┃ ┗ 📜index.html           # Main page for the Flask app
 ┣ 📜app.py                 # Flask app script
 ┣ 📜chatbot.py             # Chatbot logic using LangChain and Groq model
 ┣ 📜data.json              # Data file containing information about Diva
 ┣ 📜requirements.txt       # Python dependencies
 ┣ 📜main.ipynb             # Notebook for testing and experimentation
 ┣ 📜README.md              # Project documentation
 ┗ 📜application.py         # Main Streamlit app script
```

## 📝 How It Works

### Flask and HTML Interface

- Flask is used to serve the `index.html` page located in the `templates` directory.
- The chatbot uses a form on the HTML page to receive user queries and display responses.

### Data Processing

- The data is loaded from `data.json`, which contains key information about Diva.
- The data is processed using LangChain’s `Document` class to generate documents for the vector database.

### Vector Database

- Documents are stored in a FAISS vector database for efficient similarity searches.

### Query Handling

- The chatbot processes user queries, retrieves relevant information from the vector database using embeddings, and generates responses with the LLaMA model from Groq.

### User Interface

- The chatbot's responses and user inputs are displayed dynamically on the web page.

## 📦 Dependencies

This project requires the following dependencies, which are listed in the `requirements.txt`:

```bash
flask
streamlit
langchain
faiss-gpu
ollama-groq
```

## 📝 License

This project is licensed under the **GPLv2** - see the [LICENSE](LICENSE) file for details.

## 📬 Acknowledgments

- **Streamlit** for making data apps easy to build and deploy.


## 🧑‍💻 Author

- **Diva Gupta** – [LinkedIn](https://www.linkedin.com/in/diva-gupta-a6107421b/)
                 – [Github](https://github.com/GuptaDiva)

If you have any questions, feel free to reach out!

### 📷 Screenshots

Some screenshots from the app-
- **Flask App**-
 
![A](<Screenshot 2024-08-16 005324.png>)
![B](<Screenshot 2024-08-16 010132.png>)

- **Streamlit App**-

![A](<Screenshot 2024-08-22 002741.png>) 
![B](<Screenshot 2024-09-02 014908.png>)
