import streamlit as st
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from book_main.app.config.template import PER_TRAITS_PROMPT
from book_main.app.database.config import get_engine , load_data_from_db 
from book_main.app.utils.faiss_index import initialize_faiss_index
from book_main.app.utils.traits import PerTra, temp
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API1=os.getenv("API1")
model_name=os.getenv("EMBEDDING_MODEL")
model = SentenceTransformer(model_name)
data = load_data_from_db() 
index, book_info, data = initialize_faiss_index(data)


def main():
    st.title("Book Recommendation System")
    user_traits = st.text_area("Edit Your Traits (comma-separated):", height=4)
    if st.button("Get Recommendation"):      
        if user_traits:
            trait_list = [trait.strip() for trait in user_traits.split(",")]

            user_embeddings = [model.encode(trait).astype(np.float32) for trait in trait_list]

            book_scores = []
            for idx, row in data.iterrows():
                book_embeddings = row["Embeddings"]
                total_score = 0
                for user_embedding in user_embeddings:
                    similarities = [
                        cosine_similarity([user_embedding], [book_embedding])[0][0]
                        for book_embedding in book_embeddings
                    ]
                    max_similarity = max(similarities)
                    if max_similarity >= 0.5:
                        total_score += max_similarity

                normalized_score = (total_score / len(trait_list)) * 100

                book_scores.append(
                    (row["BookTitle"], normalized_score, row["thumbnail"], row["authors"], row["description"], row["categories"])
                )

            top_books = sorted(book_scores, key=lambda x: x[1], reverse=True)[:5]
            st.write(user_traits)
            st.subheader("Top Recommended Books")

            for title, score, thumbnail_url, author, description, categories in top_books:
                col1, col2 = st.columns([1, 3]) 
                with col1:
                    if thumbnail_url:
                        st.image(thumbnail_url, width=100)
                with col2:
                    # st.write(f"**Title**: {title} | **Normalized Similarity Score**: {score:.2f}%")
                    st.write(f"**Title**: {title}")
                    st.write(f"**Author**: {author}")
                    st.write(f"**Description**: {description}")
                    st.write(f"**Categories**: {categories}")
                st.write("---------------------")

            if not top_books:
                st.warning("No books matched your traits to recommend.")
        else:  
            st.warning("Please edit traits and click 'Generate Recommendations'.")

if __name__ == "__main__":
    main()