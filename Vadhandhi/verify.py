import streamlit as st
from langchain import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Constants
flag=0
GOOGLE_API_KEY=""  # Replace with your actual API key
persist_directory = "./chroma_db"

# Initialize Google Generative AI Embeddings
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# Function to verify news using extracted or input text
def verify_news(news_text):
    # Load from disk
    vectorstore_disk = Chroma(
        persist_directory=persist_directory,       # Directory of db
        embedding_function=gemini_embeddings      # Embedding model
    )

    retriever = vectorstore_disk.as_retriever(search_type="mmr", search_kwargs={"k": 1})

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0.3, top_p=0.85,
        google_api_key=GOOGLE_API_KEY
    )

    # Prompt template to query Gemini
    llm_prompt_template = """You are an assistant for verifying whether a news is fake or original.
    Use the following context to check whether the news given by the user and the news in databse is similar or have same context.
    If the news is present and has the same context as in the database, return True and provide relevant link.
    If the news is not present or has a different story from the one in the database, return False and provide additional data and links about the original news.
    If you don't know the answer, just say that you don't know.
    Don't try to make up an answer.
    Print a line space after returning True or False.
    Reference should be in a new line .
    Keep the answer in a simple format and not as json.\n
    News: {news} \nDatabase Context: {context} \nAnswer:"""

    llm_prompt = PromptTemplate(template=llm_prompt_template, input_variables=["context", "question"])

    # Function to format documents with metadata
    def format_docs_with_metadata(docs):
        formatted_docs = []
        for doc in docs:
            content = doc.page_content
            metadata = doc.metadata
            # Combine content and metadata into a formatted string
            formatted_doc = f"Content: {content}\nMetadata: {metadata}"
            formatted_docs.append(formatted_doc)
        return "\n\n".join(formatted_docs)

    # RAG Chain Configuration
    rag_chain = (
        {"context": retriever | format_docs_with_metadata, "news": RunnablePassthrough()}
        | llm_prompt
        | llm
        | StrOutputParser()
    )

 
    # Invoke the RAG chain with user input
    res = rag_chain.invoke(news_text)
    st.write("### Verification Result:")
    st.write(res)

    # # Show detailed documents if needed
    # if st.checkbox("Show detailed retrieved documents with metadata"):
    #     retrieved_docs = retriever.get_relevant_documents(news_text)
    #     formatted_docs = format_docs_with_metadata(retrieved_docs)
    #     st.write("### Detailed Documents:")
    #     st.text(formatted_docs)
