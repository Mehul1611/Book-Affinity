import streamlit as st
import importlib
from sqlalchemy import MetaData, Table, select, insert
from sqlalchemy.orm import sessionmaker
from book.app.database.config import get_engine  
import pandas as pd
import requests

engine = get_engine()
Session = sessionmaker(bind=engine)

def main():
    st.title("Add a New Book to the Database")
    
    with st.form(key="add_book_form"):
        new_title = st.text_input("Title")
        new_author = st.text_input("Author")
        new_description = st.text_area("Description (Optional)")

        if st.form_submit_button("Add Book"):
            with Session() as session:

                metadata = MetaData()
                metadata.reflect(bind=engine)
                books_table = metadata.tables["book"]

                check_query = select(books_table).where(
                    (books_table.c.title == new_title) &
                    (books_table.c.authors == new_author)
                )
                result = session.execute(check_query).fetchone()

                if result:
                    st.warning("This book is already present in the database!")
                else:
                    insert_query = books_table.insert().values(
                        title=new_title,
                        authors=new_author,
                        description=new_description
                    )
                    session.execute(insert_query)
                    session.commit() 
                    st.success("Book added to the database!")