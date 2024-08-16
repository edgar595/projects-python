# Python Projects Repository

Welcome to my Python projects repository! This repository contains various data analysis and machine learning projects implemented in Python. Below is an overview of each project:

## 1. LoanAmount Prediction

- **Objective**: Predict the loan amount using over 30 features.
- **Description**: This project involves predicting the loan amount based on a dataset with over 30 features. It includes data preprocessing (imputing missing values, fixing outliers), exploratory data analysis (EDA), correlation analysis, and model selection. The project settled on using Random Forest and fine-tuned it for optimal accuracy. The results are showcased using Streamlit.
- **Technologies**: Python, Scikit-learn, Pandas, Streamlit
- **Folder**: `loanamount-prediction`

## 2. Firebase Authentication and Health EDA

- **Objective**: Implement Firebase authentication and visualize exploratory health data analysis.
- **Description**: This project integrates Firebase for authentication features and includes an exploratory data analysis (EDA) of health-related data. It showcases interactive features for exploring health trends.
- **Technologies**: Python, Firebase, Streamlit, Pandas, Matplotlib
- **Folder**: `firebase-auth-health-eda`

## 3. Malaria Image Classification

- **Objective**: Classify malaria images as infected or uninfected using TensorFlow.
- **Description**: This project utilizes TensorFlow to classify malaria images into infected or uninfected categories. It includes data preprocessing, model training, and evaluation. A Streamlit dashboard is used to showcase the image classification model.
- **Technologies**: Python, TensorFlow, Streamlit, OpenCV
- **Folder**: `malaria-image-classification`

## 4. Person of Interest Image Classification

- **Objective**: Identify persons of interest using image classification techniques.
- **Description**: This project employs OpenCV for detecting eyes and frontal faces, and wavelet transforms for image classification to identify persons of interest among five different actors. It involves preprocessing, feature extraction, and model training.
- **Technologies**: Python, OpenCV, Wavelet Transform, Image Classification
- **Folder**: `person-of-interest-classification`

## 5. Question Answering with ViLT and Streamlit

- **Objective**: Answer questions from images using Vision-and-Language Transformer (ViLT) and showcase results in Streamlit.
- **Description**: This project utilizes ViLT for question answering from images. It includes model integration, question processing, and displaying results interactively using Streamlit.
- **Technologies**: Python, ViLT, Streamlit, Transformers
- **Folder**: `qa-vilt-streamlit`

## 6. Tweet Sentiment Analysis
- **Objective**: Analyze tweet sentiments to classify them as positive, negative, or neutral.
- **Description**: This project involves analyzing tweet data to classify sentiments using natural language processing (NLP) techniques. It includes data collection, preprocessing (tokenization, stop word removal, etc.), feature extraction using TF-IDF, and classification using BERT analysis and also Vader. The project results are displayed using a dash app.
- **Technologies**: Python, NLTK, Scikit-learn, BERT, dash
- **Folder**: tweet-sentiment-analysis

## 7. Kenyan Law PDF Analysis

- **Objective**: Extract and analyze text from the Constitution of Kenya PDF.
- **Description**: This project involves extracting text from the Constitution of Kenya PDF, identifying chapters and their titles, retrieving chapter content, summarizing text, and searching for specific legal provisions. It uses PyPDF2 for text extraction, regular expressions for pattern matching, and transformers for summarization. The project provides a comprehensive analysis of the constitutional text.
- **Technologies**: Python, PyPDF2, Regular Expressions, Natsort, Transformers
- **Folder**: `kenyan-law-analysis`


## 8. Resume - Ranking
- **Objective**: Rank resumes based on their similarity to a job description using machine learning techniques.
- **Description**: This project involves analyzing and ranking resumes by their relevance to a given job description and department. It uses various text processing and machine learning techniques to extract text from resumes, preprocess the text, and compute similarity scores. The application allows users to upload a job description or input text directly. The top-ranked resumes are displayed, and users can view the details of each resume through a modal interface. The project employs a Dash app to provide an interactive and user-friendly experience.
- **Technologies**: Python, TfidfVectorizer, Cosine Similarity, PyPDF2, Dash, Bootstrap
- **Folder**: resume-ranking

## 9. Protest Interface with AI-Powered Q&A

- **Objective**: Create an interactive interface for protest-related information and AI-powered question answering.
- **Description**: This project combines a visually engaging user interface with an AI-powered question answering system focused on protest-related information. It features:
  - A stylized loading screen with dynamic progress updates and system messages.
  - A main interface with a chat-like Q&A system powered by a RoBERTa-based model.
  - A "Missing Persons" section displaying profiles of individuals.
  - AI model that answers questions based on pre-defined QA pairs, date-based context, and keyword searches in a protest-related text corpus.
  - Integration with Flask for backend processing and API endpoints.
- **Technologies**: Python, Flask, HTML, CSS, JavaScript, PyPDF2, AI,Transformers (RoBERTa), NLTK, FuzzyWuzzy
- **Key Features**:
  - Dynamic loading screen with progress bar and system messages
  - AI-powered question answering system
  - Date-based and keyword-based context retrieval
  - Missing persons profile display
  - Responsive chat-like interface for user interactions
- **Folder**: intelligence-protest-interface-qa

## 10. PDF Chatbot

- **Objective**: Develop an interactive chatbot for querying PDF documents.
- **Description**: This project creates a chatbot interface for querying information from uploaded PDF files. It uses LangChain for text splitting, embedding, vector storage, and conversational retrieval. The Streamlit application allows users to upload PDFs, process them, and interact with the chatbot to get answers from the PDF content.
- **Technologies**: Python, Streamlit, PyPDF2, LangChain, Cohere, FAISS
- **Folder**: `pdf-chatbot`

## 11. Breast Cancer Prediction

- **Objective**: Predict breast cancer diagnosis using cell nuclei information.
- **Description**: This project uses machine learning to predict whether a breast mass is benign or malignant based on cell nuclei measurements. It features an interactive Streamlit interface with adjustable sliders for various cell measurements, a radar chart visualization of the input data, and a prediction output with probability scores. The app can be connected to a cancer lab to assist in diagnosing breast cancer from tissue samples.
- **Key Features**:
  - Interactive sidebar with sliders for adjusting cell nuclei measurements
  - Radar chart visualization of mean, standard error, and worst values for various cell characteristics
  - Machine learning model integration for cancer prediction
  - Probability scores for benign and malignant outcomes
  - Responsive design with custom CSS styling
- **Technologies**: Python, Streamlit, Pandas, Plotly, Scikit-learn, Pickle
- **Folder**: `Cancer`

## 12. Chat with MySQL
- **Objective**: Interact with a MySQL database using a chat interface.
- **Description**: This project creates a chat interface for interacting with a MySQL database. Users can ask SQL-related questions, and the application generates SQL queries based on the database schema and conversation history. The Streamlit app provides a user-friendly chat interface for querying the database and receiving natural language responses.
- **Technologies**: Python, Streamlit, LangChain, Cohere, MySQL
- **Folder**: chat-with-mysql