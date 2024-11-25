import streamlit as st
from sqlalchemy import MetaData, select, Table
from sqlalchemy.orm import sessionmaker
from book_main.utils.db_utils import database

class BookManager:
    def __init__(self):
        self.engine = database.get_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine, schema="public")
        self.books_table = Table("book", self.metadata, autoload_with=self.engine, schema="public")

    def add_book(self, title, author, description):
        """Add a new book to the database."""
        with self.Session() as session:
            check_query = select(self.books_table).where(
                (self.books_table.c.title == title) &
                (self.books_table.c.authors == author)
            )
            result = session.execute(check_query).fetchone()

            if result:
                return "warning", "This book is already present in the database!"
            else:
                
                insert_query = self.books_table.insert().values(
                    title=title,
                    authors=author,
                    description=description
                )
                session.execute(insert_query)
                session.commit()
                return "success", "Book added to the database!"

    def render_form(self):
        """Render the Streamlit form for adding a new book."""
        st.title("Add a New Book to the Database")
        
        with st.form(key="add_book_form"):
            new_title = st.text_input("Title")
            new_author = st.text_input("Author")
            new_description = st.text_area("Description (Optional)")

            if st.form_submit_button("Add Book"):
                status, message = self.add_book(new_title, new_author, new_description)
                if status == "warning":
                    st.warning(message)
                elif status == "success":
                    st.success(message)

manager = BookManager()
