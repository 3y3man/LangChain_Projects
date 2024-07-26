# Import necessary libraries
import atexit
import os
import streamlit as st
from dotenv import load_dotenv 
from langchain import hub
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables i.e. OpenAI's API Key
# load_dotenv()

DATA_PATH = "data/"

os.makedirs(DATA_PATH, exist_ok=True)

# Function to list files in the data folder
def list_files():
    return os.listdir(DATA_PATH)

# Function to remove all files in the data folder
def clear_data_folder():
    for file_name in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

# Register the cleanup function to be called when the app stops running
atexit.register(clear_data_folder)

st.title("READ MY DOCS!📄")

os.environ["OPENAI_API_KEY"] = st.sidebar.text_input("Enter your API key", type='password')
upload_file = st.sidebar.file_uploader("# Upload your documents here;", type=["pdf", "txt", "docx"], accept_multiple_files=True)
if upload_file:
    for uploaded_file in upload_file:
        file_path = os.path.join(DATA_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"Saved files: {[file.name for file in upload_file]}")
    
    
# Display the list of files in the data folder
st.sidebar.subheader("Files in data folder:")
files = list_files()
if files:
    for file in files:
        st.sidebar.write(file)
else:
    st.sidebar.write("No files found.")

# Optional: Add a button to manually clear the data folder
if st.sidebar.button("Clear data folder"):
    clear_data_folder()
    st.rerun()
    
if not os.listdir(DATA_PATH):
    st.warning("Upload a text file to begin")
else: 
    llm = ChatOpenAI(model="gpt-3.5-turbo-0613")

    # LOAD
    loader = DirectoryLoader(DATA_PATH)
    docs = loader.load()

    # SPLIT
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # STORE
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # RAG
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question based on your documents?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = rag_chain.invoke(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
