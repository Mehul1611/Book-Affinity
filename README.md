# Book-Affinity

This project is designed to extract personality traits from book summaries using the Groq API, process the results, and store them in a PostgreSQL database. The project leverages SQLAlchemy for database interaction and environment variables for secure API key management. It supports trait extraction based on predefined traits, integrates with a PostgreSQL database, and performs data handling without the need for CSV files.

## Features
- **Extract Traits**: Use Groq's LLM model to extract personality traits of user and recommend on basis of traits extracted from book summaries.
- **Database Integration**: Store extracted traits in a PostgreSQL database for easy querying and future use.
- **Environment Variable Support**: Store sensitive information (API keys, model names, and database connection strings) securely using `.env` files.
- **Error Handling**: Proper error handling for failed API requests.

## Requirements
- Python 3.7+
- PostgreSQL Database (or any supported SQL database)
- Required Python libraries:
  - `requests`
  - `SQLAlchemy`
  - `psycopg2-binary`
  - `python-dotenv`
  - `faiss`
    

## Installation

### Clone the repository

cd book-trait-extraction
To install Project, follow these steps:
1. Clone the repository: **`git clone https://github.com/Mehul1611/Book-Affinity.git`**
2. Navigate to the project directory: **`cd recipe_recommendation`**
3. Install dependencies: **`pip install -r requirements.txt`**
4. Create a **`.env`** file in the project directory and add your Groq API key:**`GROQ_API_KEY=your_api_key_here`**
5. Run the application:**`streamlit run app.py`**
