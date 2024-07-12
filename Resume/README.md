## Resume - Ranking

**Introduction**
This project aims to automate the ranking of resumes based on their relevance to a given job description using machine learning techniques. It utilizes text processing and cosine similarity to analyze resumes and compute similarity scores against the job description. The project is implemented as a Dash web application, providing an interactive interface for users to upload a job description or input text directly. The top-ranked resumes are displayed, allowing users to view details and summaries through a modal interface.

**Installation**

### Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system
- Stable internet connection for dependencies

### Setup
1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/resume-ranking.git
    cd resume-ml-ranking
    ```

2. **Create a Virtual Environment**
    It’s recommended to create a virtual environment for the project. Use the following commands:
    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```

3. **Install Dependencies**
    Install required Python packages using pip:
    ```sh
    pip install -r requirements.txt
    ```

**Usage**
Here’s how to use the Resume ML Ranking tool:

1. **Starting the Application**
    To start the Dash application, run:
    ```sh
    python app.py
    ```
    This will start the application on your local server.

2. **Uploading a Job Description**
    - Paste or upload a job description into the input field provided.
    - Click on the "Submit" button to initiate the ranking process.

3. **Viewing Ranked Resumes**
    - The application will display the top-ranked resumes based on similarity scores.
    - Click on resume links to view detailed summaries in a modal.

**Features**
- Automatically ranks resumes based on similarity to a job description
- Uses TF-IDF vectorization and cosine similarity for scoring
- Provides an interactive interface with Dash for ease of use
- Supports uploading job descriptions and viewing resume details

---

This README provides an overview of the Resume - ML - Ranking project, guiding users on installation, usage, features, and licensing information. Adjust paths, commands, and details as per your project structure and requirements.
