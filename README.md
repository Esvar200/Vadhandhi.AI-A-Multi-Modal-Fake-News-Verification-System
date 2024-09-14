# Vadhandhi.AI-A-Multi-Modal-Fake-News-Verification-System
**Multi-Modal Fake News Verification System** is an advanced tool designed to verify the authenticity of news using text, image, and audio inputs. The system leverages the Retrieval-Augmented Generation (RAG) approach to detect fake news by comparing user-provided content against legitimate news sources.

## Key Features

- **Retrieval-Augmented Generation (RAG) Approach**: The system integrates RAG to enhance the verification process by combining retrieved relevant news articles with generative capabilities for a comprehensive analysis.
- **Text Verification**: Extracts keywords from the news text and searches for related articles using the GoogleNews library. The retrieved articles are stored in Chroma DB for further comparison.
- **Image Verification**: Utilizes EasyOCR to extract text from images, which is then processed similarly to textual input using the RAG approach.
- **Audio Verification**: Converts audio input to text using a speech recognition library, which is then compared with legitimate news articles retrieved using the RAG approach.
- **Cross-Modal Comparison**: Leverages the Gemini LLM to perform a final comparison between the extracted text and the legitimate news articles. The model returns a verification result (true or false), along with additional links to relevant information.

## Technologies Used

- **GoogleNews Library**: For retrieving relevant news articles based on extracted keywords.
- **Chroma DB**: A vector database for storing and retrieving search results.
- **EasyOCR**: For extracting text from images.
- **Speech Recognition**: For converting audio input to text.
- **Gemini LLM**: For generating a comprehensive comparison and determining the authenticity of the news.
- **RAG (Retrieval-Augmented Generation)**: Combines the retrieval of relevant documents with generative models to enhance the accuracy of fake news detection.

## How to Run the Project

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Esvar200/Vadhandhi.AI-A-Multi-Modal-Fake-News-Verification-System
    cd Vadhandhi.AI-A-Multi-Modal-Fake-News-Verification-System
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Main Application**:
    ```bash
    streamlit run app.py
    ```

4. **Follow the On-Screen Instructions**:
   - Provide the news input in text, image, or audio format (only .wav for audio and .jpg, .jpeg, .png for images)
   - The system will process the input using the RAG approach and display whether the news is true or false, along with additional links for further verification.

## File Structure

- **`app.py`**: The main application file that coordinates the entire verification process.
- **`verify.py`**: Verifies the news and prints the results after comparison.
- **`audio_process.py`**: Converts audio input to text and sends it to text processing.
- **`image_process.py`**: Extracts text from images and processes it using the same flow as audio.
- **`text_process.py`**: Searches keywords using the Google News library, updates the Chroma DB, and sends data to `verify.py` for further verification.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any feature enhancements or bug fixes.
---
