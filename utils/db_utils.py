import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from book_main.utils.db_query import QUESTION_ANSWER, DATA_LOAD, FETCH_DATA
from book_main.constant import DATABASE_URL

class DatabaseHandler:
    def __init__(self):
        self.engine = self.get_engine()


    def get_engine(self):
        db_url = DATABASE_URL
        return create_engine(db_url)


    def save_to_db(self, book_title, questions_and_answers):
        query = QUESTION_ANSWER
        data_to_insert = [
            {   
                "book_title": book_title,
                "question": qa["question"],
                "suggestions": ", ".join(qa["suggestions"]),
                "user_answer": qa["answer"],
                "created_at": datetime.now()
            }
            for qa in questions_and_answers
        ]
        self._execute_query(query, data_to_insert)


    def _execute_query(self, query, data):
        with self.engine.connect() as connection:
            for entry in data:
                connection.execute(text(query), entry)
                connection.commit()


    def load_data_from_db(self):
        query = DATA_LOAD
        return pd.read_sql(query, self.engine)


    def fetch_last_entries(self):
        query = text(FETCH_DATA)
        with self.engine.connect() as connection:
            result = connection.execute(query).fetchall()
            return self._format_results(result)


    def _format_results(self, result):
        if result:
            columns = result[0].keys() if hasattr(result[0], 'keys') else [
                'book_title', 'question', 'suggestions','user_answer', 'created_at']
            return pd.DataFrame(result, columns=columns)
        return pd.DataFrame(columns=['book_title', 'question', 'suggestions','user_answer', 'created_at'])

database=DatabaseHandler()
