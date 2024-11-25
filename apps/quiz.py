import streamlit as st
from book_main.llm.question_generation import generate_questions, generate_summary
from book_main.utils.traits_function import recommender
from book_main.apps.reccomendation import recommendation_system
from book_main.utils.db_utils import database

class Quiz:
    def __init__(self):
        if "questions" not in st.session_state:
            st.session_state.questions = []
        if "answers" not in st.session_state:
            st.session_state.answers = []
        self.book_title = ""
        self.questions_and_answers = []

    def render_header(self):
        st.header('Book Questionnaire')

    def generate_questionnaire(self):
        if self.book_title:
            with st.spinner("Generating questionnaire..."):
                summary = generate_summary(self.book_title)
                questionnaire = generate_questions(self.book_title)

                if summary and questionnaire:
                    st.subheader("Summary")
                    st.write(summary)
                    st.session_state.questions = questionnaire
                    st.session_state.answers = [""] * len(questionnaire)
                else:
                    st.error("No relevant information found for the book.")
        else:
            st.warning("Please enter a book title.")

    def display_questionnaire(self):
        if st.session_state.questions:
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
                self.questions_and_answers.append({
                    "question": question_text,
                    "suggestions": suggestions,
                    "answer": user_answer
                })

    def save_answers(self):
        if st.button("Submit Answers"):
            engine = database.get_engine()
            database.save_to_db(self.book_title, self.questions_and_answers)
            st.success(f"Your answers have been saved!")

    def get_recommendations(self):
        if st.button("Get Recommendation"):
            user_traits = recommender.perso_trait()
            traits_str = ", ".join(user_traits)
            st.write(traits_str)
            recommendation_system.recommend_books(traits_str)
    
    def runner(self):
        self.render_header()
        self.book_title = st.text_input("Enter the book title:")
        if st.button("Generate Questionnaire"):
            self.generate_questionnaire()
        if st.button("Skip Questionnaire"):
            st.session_state.app_selection = "Recommender"
            st.rerun()
        self.display_questionnaire()
        self.save_answers()
        self.get_recommendations()

quest = Quiz()