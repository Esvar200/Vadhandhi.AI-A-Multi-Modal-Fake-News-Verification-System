import streamlit as st
from datetime import datetime, timedelta
from GoogleNews import GoogleNews
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from verify import verify_news

GOOGLE_API_KEY=""  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")
persist_directory = "./chroma_db"

# Initialize Google Generative AI Embeddings
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# Initialize Chroma vectorstore with persistence enabled
vectorstore = Chroma(embedding_function=gemini_embeddings, persist_directory=persist_directory)

# Function to process text input
def process_text_input(inp_query,flag):
    if(flag==0):
        inp_query = st.text_input("Enter the query:")
    prompt = f"Extract the most important keywords from the following text: {inp_query}"
    search_keyword = model.generate_content(prompt)

    # Date input
    start_date = st.text_input("Enter the start date (MM/DD/YYYY) or leave blank for default period (last 3 days):")
    end_date = st.text_input("Enter the end date (MM/DD/YYYY) or leave blank for default period (last 3 days):")

    # Convert dates or set default date range
    if not start_date and not end_date:
        end_date = datetime.now().strftime('%m/%d/%Y')
        start_date = (datetime.now() - timedelta(days=3)).strftime('%m/%d/%Y')

    if st.button("Search News"):
        with st.spinner("Processing..."):
            # Initialize GoogleNews object and set the date range
            googlenews = GoogleNews()
            googlenews.set_time_range(start_date, end_date)

            # Search for the keyword
            googlenews.search(search_keyword.text)
            result = googlenews.result()

            # Check and handle empty or missing data
            for news in result:
                news['title'] = news.get('title', 'No title available')
                news['date'] = news.get('date', 'No date available')
                news['link'] = news.get('link', '#')
                news['desc'] = news.get('desc', 'No description available')

            # Print the top 2 search results in Streamlit
            if result:
                for news in result[:2]:  # Show only top 2 results
                    st.write(f"**Title:** {news['title']}")
                    st.write(f"**Date:** {news['date']}")
                    st.write(f"**Link:** {news['link']}")
                    st.write(f"**Description:** {news['desc']}")
                    st.write("-" * 40)

                # Update Chroma DB with the fetched news data
                for news in result:
                    text_content = news.get("desc", "No description available")  # Use default if description is missing
                    url = news.get("link", "#")  # Use default if URL is missing
                    title = news.get("title", "No title available")  # Use default if title is missing
                    date = news.get("date", "No date available")  # Use default if date is missing

                    # Ensure text_content is not empty before processing
                    if text_content.strip():  # Process only if there's content
                        # Create a Document object with full metadata
                        docs = [Document(
                            page_content=text_content,
                            metadata={
                                "URL": url,
                                "Title": title,
                                "Date": date
                            }
                        )]
                        
                        # Add or update documents in Chroma DB
                        vectorstore.add_documents(docs)
                    else:
                        st.warning(f"Skipped empty content for news with title: {title}")

                # Save the updated state to disk
                vectorstore.persist()
                st.success("Chroma DB updated successfully with fetched news data!")
            if inp_query.strip():        
                verify_news(inp_query)            
