# Protest Interface Web Application

This web application provides an interface to ask questions about protests in Kenya and get accurate answers. It includes a chat interface with a loading screen, and answers questions using a combination of predefined answers and a machine learning model. The question-answering functionality relies on a combination of the following components: Predefined Answers, Machine Learning Model this model is fine-tuned on data related to Kenyan protests to provide contextually accurate answers., Key Terms and Fuzzy Matching,Date Parsing which the application uses dateutil to parse and handle dates within the questions. This is particularly useful for questions related to specific events or timelines of the protests.

## Features

- **Loading Screen:** A visually appealing loading screen while the AI model loads.
- **Chat Interface:** Users can ask questions related to Kenyan protests and get answers.
- **Predefined and Model-Based Answers:** Uses a mix of predefined answers and a machine learning model to provide accurate responses.

## Demo

### Loading Screen

![Loading Screen GIF](static/images/vid.gif)

### Question Answering

1. **Question 1:**
    - ![Question 1 Video](link-to-question-1-video)
2. **Question 2:**
    - ![Question 2 Video](link-to-question-2-video)

### Prerequisites

- Python 3.10
- Flask
- PyPDF2
- Transformers
- Torch
- FuzzyWuzzy
- NLTK
- Dateutil


## Data and Context
# Protest Data:

The application includes detailed data about Kenyan protests, including dates, events, and casualties. This data is stored in a structured format that the application can query to provide specific answers.
The data is continuously updated to include the latest information and ensure that the answers remain accurate and relevan

# Context-Based Answers:

- The application is designed to provide context-based answers, meaning it can understand and respond to questions that require knowledge of specific events or timelines.
- The combination of predefined answers and the machine learning model allows the application to handle a wide range of questions with varying levels of complexity.