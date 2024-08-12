# PDF QA Chatbot Project

## Project Overview
This project is a PDF Question-Answering (QA) chatbot that allows users to interact with PDF documents by asking questions and receiving relevant answers. The chatbot leverages advanced language models from Cohere and incorporates them into a Streamlit application to provide an intuitive and interactive experience.

## Key Features
- **PDF Text Extraction:** Extracts text from uploaded PDF documents.
- **Text Chunking:** Splits the extracted text into manageable chunks for processing.
- **Conversational Retrieval:** Utilizes Cohere's language model for answering questions based on the context of the provided PDFs.
- **Interactive UI:** A user-friendly interface built with Streamlit, offering a chat-like experience for asking questions and receiving answers.

## Data Processing

### PDF Text Extraction
- **Libraries Used:** `PyPDF2` is employed to extract text from the uploaded PDF documents.
- **Methodology:** The entire text from each page of the PDFs is read and concatenated to form a single string for further processing.

### Text Chunking
- **Purpose:** To manage the large size of PDF documents, the text is split into smaller chunks.
- **Technique:** Utilizes `CharacterTextSplitter` from the LangChain library to chunk the text into sections of 1000 characters with a 200-character overlap.

### Conversational Retrieval
- **Embeddings:** Uses CohereEmbeddings to convert text chunks into embeddings for semantic search.
- **Vector Store:** FAISS is used to store and retrieve these embeddings, allowing the model to find relevant text chunks based on user queries.
- **Conversational Chain:** Combines the language model with a conversational memory to maintain context across multiple queries.

## Modeling

### Cohere Language Model
- **API Integration:** The project relies on Cohere's API for accessing their language models.
- **Usage:** The model is utilized to generate contextually accurate responses to user queries based on the content of the uploaded PDFs.
- **API Key Requirement:** Users must have a valid Cohere API key to use the chatbot's features. This key is essential for authentication and access to Cohere's language processing capabilities.

## Application Features

### Streamlit Interface
- **User Input:** A text input field allows users to ask questions related to the content of the uploaded PDFs.
- **Response Display:** The chatbot's answers are displayed in a conversational format, mimicking a chat interface with distinct user and bot message styling.
- **Sidebar:** Users can upload multiple PDF documents, which are then processed in bulk for text extraction and analysis.

### Loading Messages
- **UI Enhancements:** The application includes dynamic messages indicating the model's loading state, improving the user experience by notifying when the model is ready for interaction.

## Project Demonstration
- **[Project Demonstration](https://pdf-question-answering.streamlit.app/):** A detailed walkthrough of the chatbot's functionality, showcasing real-time PDF interaction and question answering.

## Getting Started

### Prerequisites
- **Python 3.10+**
- **Streamlit**
- **Cohere API Key:** Ensure you have a valid API key from Cohere to access their language models.
