import streamlit as st
import importlib
import os
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from book_main.utils.db_utils import DatabaseHandler
from book_main.apps.home import manager
from book_main.apps.reccomendation import recommendation_system
from book_main.apps.user_preference import recommender
from book_main.apps.quiz import quest


class StreamlitApp:

    def __init__(self):
        load_dotenv()
        self.database = DatabaseHandler()
        self.engine = self.database.get_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        style = os.getenv("STYLE_PATH")
        self.load_style(style)


    def load_style(self, style_path):
        try:
            with open(style_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Failed to load style: {e}")


    def app_selection_function(self):
        if "app_selection" not in st.session_state:
            st.session_state.app_selection = "Home"  
        app_selection = st.selectbox(
            "Choose App", ["Home","Preference", "Quiz", "Recommender"],
            index=["Home","Preference", "Quiz", "Recommender"].index(st.session_state.app_selection)
            )
        if app_selection == "Home":
            manager.render_form() 
        elif app_selection == "Quiz":
            quest.runner()
        elif app_selection == "Recommender":
            recommendation_system.runner()
        elif app_selection == "Preference":
            recommender.loader()


if __name__ == "__main__":
    app = StreamlitApp()
    app.app_selection_function()