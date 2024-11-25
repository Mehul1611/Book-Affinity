import streamlit as st
from book_main.llm.prompt import PER_TRAITS_PROMPT
from book_main.utils.db_utils import database
from book_main.llm.question_generation import call_groq_api

class BookRecommender:
    def __init__(self):
        self.data = database.load_data_from_db()  
    
    def perso_trait(self):
        """Function to fetch user answers, process them and call the Groq API."""
        df = database.fetch_last_entries()
        if df.empty:
            st.warning("No recent entries found in the database.")
            return None

        user_answers = df['user_answer'].tolist()
        book_title = df['book_title'].iloc[0]
        questions = df['question']
        analysis_prompt = PER_TRAITS_PROMPT.format(book_title=book_title, user_answers=user_answers, questions=questions)

        traits_summary = call_groq_api(analysis_prompt)
        return traits_summary
    
recommender = BookRecommender()