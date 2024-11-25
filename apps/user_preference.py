import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from book_main.utils.db_utils import database
from book_main.constant import MODEL
from book_main.utils.embeddings import manager
from urllib.parse import quote

class BookRecommendation:
    def __init__(self):
        self.data = database.load_data_from_db()

    def encode_user_preferences(self, preferences):
        pref_list = [pref.strip() for pref in preferences.split(",") if pref.strip()]
        return [MODEL.encode(pref).astype(np.float32) for pref in pref_list]


    def calculate_similarity(self, user_embeddings, book_embeddings):
        total_score = 0
        for user_embedding in user_embeddings:
            similarity_scores = [
                cosine_similarity([user_embedding], [book_embedding])[0][0]
                for book_embedding in book_embeddings
            ]
            total_score += max(similarity_scores)
        return total_score


    def get_recommendations(self, preferences):
        previous=set()
        user_embeddings = self.encode_user_preferences(preferences)
        recommended_books = []
        for _, row in self.data.iterrows():
            book_title = row["BookTitle"]
            if book_title not in previous:
                book_embeddings = manager.fetch_categories(book_title)
                if book_embeddings:
                    score = self.calculate_similarity(user_embeddings, book_embeddings)
                    recommended_books.append(
                        (
                            row["BookTitle"],
                            score,
                            row.get("thumbnail"),
                            row.get("authors"),
                            row.get("description"),
                            row.get("categories"),))
                    previous.add(row["BookTitle"])
            else:
                continue
        return recommended_books


    def display_recommendations(self, books):
        st.subheader("Top Recommended Books")
        for title, score, thumbnail, author, description, categories in books:
            col1, col2 = st.columns([1, 3])
            with col1:
                if thumbnail:
                    st.image(thumbnail, width=100)
            with col2:
                st.write(f"**Title**: [{title}](https://www.goodreads.com/search?query={quote(title)})")
                st.write(f"**Author**: {author}")
                st.write(f"**Description**: {description}")
                st.write(f"**Categories**: {categories}")
            st.write("---------------------")


    def recommend_books(self, preferences):
        if not preferences:
            st.warning("Please provide your reading preferences.")
            return
        books = self.get_recommendations(preferences)
        top_books = sorted(books, key=lambda x: x[1], reverse=True)[:5]

        if top_books:
            self.display_recommendations(top_books)
        else:
            st.warning("No books matched your preferences.")


    def loader(self):
        st.title("Personalized Book Recommendation System")
        st.subheader("Tell us your reading preferences")
        Genre = st.text_input("Genre (e.g., business, fantasy, mystery)")
        topic = st.text_input("Topic (e.g., finance, technology, travel)")
        if st.button("Get Recommendation"):
            preferences = ", ".join([input_field for input_field in [Genre, topic] if input_field.strip()])
            if preferences:
                self.recommend_books(preferences)
            else:
                st.warning("Please fill at least one field to get recommendations.")


recommender = BookRecommendation()