import streamlit as st
from groq import Groq
import csv
import os
from book_main.app.config.template import QUESTION_PROMPT, SUMMARY_PROMPT
from dotenv import load_dotenv
import pandas as pd
from book_main.app.utils.question import generate_questions, generate_summary
from book_main.app.utils.reccomendation import  main
from book_main.app.utils.traits import PerTra, temp
from book_main.app.database.config import get_engine, save_to_db 
import requests
import csv
from datetime import datetime
from sqlalchemy import text

load_dotenv()
API1=os.getenv("API1")
api_key = API1
client = Groq(api_key=api_key)
engine = get_engine()


# Streamlit UI
def main_book():
    st.header('Book Questionare')
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = []

    book_title = st.text_input("Enter the book title:")

    if st.button("Generate Questionnaire"):
        if book_title:
            with st.spinner("Generating questionnaire..."):
                summary = generate_summary(book_title)
                questionnaire = generate_questions(book_title)

                if summary and questionnaire:
                    st.subheader("Summary")
                    st.write(summary)
                    st.session_state.questions = questionnaire
                    st.session_state.answers = [""] * len(questionnaire)

                else:
                    st.error("No relevant information found for the book.")
        else:
            st.warning("Please enter a book title.")
    if st.button("Skip Questionnaire"):
        st.session_state.app_selection = "Recommender"
        st.rerun() 
    if st.session_state.questions:
        questions_and_answers = []

        for idx, question in enumerate(st.session_state.questions):
            parts = question.split("\n")
            question_text = parts[0]
            suggestions = parts[1:4]  

            st.write(f"**Question :** {question_text}")
            st.write("**Suggestions:**")

            selected_suggestion = st.radio(
                f"Choose an answer for question {idx + 1}:",
                options=suggestions + ["Other (Type your own)"],
                key=f"radio_{idx}"
            )

            if selected_suggestion == "Other (Type your own)":
                user_answer = st.text_input(
                    f"Type your own answer for question {idx + 1}:",
                    key=f"text_input_{idx}"
                )
            else:
                user_answer = selected_suggestion

            st.session_state.answers[idx] = user_answer  

            questions_and_answers.append({
                "question": question_text,
                "suggestions": suggestions,
                "answer": user_answer
            })

        if st.button("Submit Answers"):

            save_to_db(book_title, questions_and_answers, engine)
            st.success(f"Your answers have been saved!")
        if st.button("Get Reccomendation"):
            user_answer=PerTra()
            user_answer=", ".join(user_answer)
            recco=temp(user_answer)
            st.write(recco)
if __name__ == "__main_book__":
    main_book()