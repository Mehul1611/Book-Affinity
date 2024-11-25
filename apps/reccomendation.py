import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from book_main.utils.db_utils import database
from book_main.constant import MODEL
from book_main.utils.embeddings import manager
from urllib.parse import quote


class BookRecommendationSystem:
    def __init__(self):
        self.data = database.load_data_from_db()

    def get_user_embeddings(self, trait_list):
        return [MODEL.encode(trait).astype(np.float32) for trait in trait_list]

    def calculate_similarity_score(self, user_embeddings, book_embeddings):
        total_score = 0
        for user_embedding in user_embeddings:
            sim = [
                cosine_similarity([user_embedding], [book_embedding])[0][0]
                for book_embedding in book_embeddings
            ]
            total_score += max(sim)
        return total_score

    def get_book_scores(self, user_traits):
        previous=set()
        trait_list = [trait.strip() for trait in user_traits.split(",")]
        user_embeddings = self.get_user_embeddings(trait_list)
        book_scores = []
        for idx, row in self.data.iterrows():
            book_id = row["BookTitle"]
            if len(trait_list) == 1:
                threshold = 0.9  
            else:
                threshold = 0.3 * len(trait_list)
            if book_id not in previous:
                book_embeddings = manager.fetch_embeddings(book_id)
                if book_embeddings:
                    total_score = self.calculate_similarity_score(user_embeddings, book_embeddings)
                    if total_score >threshold:
                        book_scores.append(
                        (
                            row["BookTitle"],
                            total_score,
                            row.get("thumbnail"),
                            row.get("authors"),
                            row.get("description"),
                            row.get("categories"),))
                        previous.add(row["BookTitle"])
        return book_scores

    def display_top_books(self, top_books):
        st.subheader("Top Recommended Books")
        for title, score, thumbnail_url, author, description, categories in top_books:
            col1, col2 = st.columns([1, 3])
            with col1:
                if thumbnail_url:
                    st.image(thumbnail_url, width=100)
            with col2:
                st.write(f"**Title**: [{title}](https://www.goodreads.com/search?query={quote(title)})")
                st.write(f"**Author**: {author}")
                st.write(f"**Description**: {description}")
                st.write(f"**Categories**: {categories}")
            st.write("---------------------")

    def recommend_books(self, user_traits):
        if not user_traits:
            st.warning("Please edit traits and click 'Generate Recommendations'.")
            return
        book_scores = self.get_book_scores(user_traits)
        top_books = sorted(book_scores, key=lambda x: x[1], reverse=True)[:5]
        if top_books:
            self.display_top_books(top_books)
        else:
            st.warning("No books matched your traits to recommend.")
    
    def runner(self):
        st.title("Book Recommendation System")
        user_traits = st.text_area("Edit Your Traits (comma-separated):", height=4)
        if st.button("Get Recommendation"):
            recommendation_system.recommend_books(user_traits)


recommendation_system = BookRecommendationSystem()