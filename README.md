# Book-Affinity

This project is designed to extract personality traits from book summaries using the Groq API, process the results, and store them in a PostgreSQL database. The project leverages SQLAlchemy for database interaction and environment variables for secure API key management. It supports trait extraction based on predefined traits, integrates with a PostgreSQL database, and performs data handling without the need for CSV files.

## Features
- **Add New Books**: Add books by providing their title and author.
- **Quiz-based Recommendations**: Take a quiz based on a book’s themes and traits, and receive personalized book recommendations.
- **Trait Extraction**: Use Groq's LLM model to extract personality traits from book summaries.
- **Database Integration**: Store books and recommendations in a PostgreSQL database.
- **Environment Variable Support**: Store sensitive information (API keys, model names, and database connection strings) securely using `.env` files.
- **Error Handling**: Proper error handling for failed API requests.

## Requirements
- Python 3.7+
- PostgreSQL Database (or any supported SQL database)
- Required Python libraries: **`pip install -r requirements.txt`**
    
## Installation

### Clone the repository

cd book-trait-extraction
To install Project, follow these steps:
1. Clone the repository: **`git clone https://github.com/Mehul1611/Book-Affinity.git`**
2. Navigate to the project directory: **`cd Book-Affinity`**
4. Create a **`.env`** file in the project directory and add your Groq API key:**`API1=your_api_key_here`**
5. Run the application:**`streamlit run main.py`**

## **Contributing**
Contributions are welcome! If you want to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

## **Contact**
For any questions or feedback, feel free to contact [mehulsharma1116@gmail.com](mailto:mehulsharma1116@gmail.com).
