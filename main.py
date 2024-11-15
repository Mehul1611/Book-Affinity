import streamlit as st
import importlib
from groq import Groq
from sqlalchemy import MetaData, Table, select, insert
from sqlalchemy.orm import sessionmaker
from book_main.app.database.config import get_engine
import os 
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

app1 = importlib.import_module("book_main.app.utils.quiz")  
app2 = importlib.import_module("book_main.app.utils.reccomendation")
app3 = importlib.import_module("book_main.app.utils.preference")
app4 = importlib.import_module("book_main.app.utils.home")

engine = get_engine()
Session = sessionmaker(bind=engine)
metadata = MetaData()  
metadata.reflect(bind=engine)  
style=os.getenv("STYLE_PATH")
books_table = metadata.tables["book"] 

with open(style) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if "app_selection" not in st.session_state:
    st.session_state.app_selection = "Home"  
app_selection = st.selectbox(
    "Choose App", ["Home","Preference", "Quiz", "Recommender"],
    index=["Home","Preference", "Quiz", "Recommender"].index(st.session_state.app_selection)
    )

if app_selection == "Home":
    app4.main()
elif app_selection == "Quiz":
    app1.main_book()  
elif app_selection == "Recommender":
    app2.main()
elif app_selection=="Preference":
    app3.main()
