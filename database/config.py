from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import text

load_dotenv()

# Database configuration
def get_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(db_url)

def save_to_db(book_title, questions_and_answers, engine):

    engine = get_engine()

    query = """
        INSERT INTO questionnaire_answers (book_title, question, suggestions, user_answer, created_at)
        VALUES (:book_title, :question, :suggestions, :user_answer, :created_at)
    """
    data_to_insert = [
        {   
            "book_title": book_title,
            "question": qa["question"],
            "suggestions": ", ".join(qa["suggestions"]),  # Join suggestions as a string
            "user_answer": qa["answer"],
            "created_at": datetime.now()
        }
        for qa in questions_and_answers
    ]

    with engine.connect() as connection:
        for data in data_to_insert:
            connection.execute(text(query), data)
            connection.commit()
    return None


def load_data_from_db():
    engine = get_engine() 
    query = """
    SELECT bt."BookTitle", bt."Traits", b."thumbnail", b."authors", b."description", b."categories" 
    FROM book_traits bt
    JOIN book b ON bt."BookTitle" = b."title"
    """
    data = pd.read_sql(query, engine)
    return data


def fetch_last_entries():
    engine = get_engine()
    query = text("SELECT * FROM questionnaire_answers ORDER BY created_at DESC LIMIT 10")
    with engine.connect() as connection:
        result = connection.execute(query).fetchall()
        if result:
            # Extract column names from metadata if available, else set manually
            columns = result[0].keys() if hasattr(result[0], 'keys') else [
                'id','book_title', 'question', 'suggestions','user_answer', 'created_at']
            
            # Convert result to DataFrame
            df = pd.DataFrame(result, columns=columns)
        else:
            df = pd.DataFrame(columns=[ 'id','book_title', 'question', 'suggestions','user_answer', 'created_at'])  # Empty DataFrame
    return df