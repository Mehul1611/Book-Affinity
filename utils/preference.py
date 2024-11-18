import streamlit as st
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from book.app.database.config import get_engine  , load_data_from_db
from book.app.utils.faiss_index import fetch_data_for_faiss
from book.app.config.template import RECOMMENDATION_PROMPT  
import os
import requests
import requests
from dotenv import load_dotenv

load_dotenv()
API1=os.getenv("GROQ_API_KEY")
model_name=os.getenv("EMBEDDING_MODEL")
llm_name=os.getenv("LLM_MODEL_NAME")
model = SentenceTransformer(model_name)

def temp(user_traits, book_info, trait_embeddings, category_embeddings):
    if user_traits:
        trait_list = [trait.strip() for trait in user_traits.split(",")]
        user_embeddings = [model.encode(trait).astype(np.float32) for trait in trait_list]
        book_scores = []
        for idx, book_title in enumerate(book_info):
            book_trait_embeddings = trait_embeddings[idx]
            book_categories = category_embeddings[idx]

            total_score = 0
            for user_embedding in user_embeddings:
                similarities = [
                    cosine_similarity([user_embedding], [book_embedding])[0][0]
                    for book_embedding in book_trait_embeddings
                ]
                max_similarity = max(similarities)
                if max_similarity >= 0.5:
                    total_score += max_similarity

            category_similarity = len(set(user_traits.split(",")) & set(book_categories)) / len(set(book_categories))
            final_score = total_score * 0.7 + category_similarity * 0.3 
            normalized_score = (final_score / len(trait_list)) * 100
            book_scores.append(
                (book_info["BookTitle"], normalized_score, book_info["thumbnail"], book_info["authors"], book_info["description"], book_info["categories"])
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
                    st.write(f"**Title**: {title}") 
                    st.write(f"**Author**: {author}")
                    st.write(f"**Description**: {description}")
                    st.write(f"**Categories**: {categories}")
                st.write("---------------------")

            if not top_books:
                st.warning("No books matched your traits to recommend.")
    else:  
        st.warning("Please edit traits and click 'Generate Recommendations'.")

data = load_data_from_db()
book_info, trait_embeddings, category_embeddings = fetch_data_for_faiss()

def main():
    st.title("Personalized Book Recommendation System")
    st.subheader("Tell us your reading preferences")
    mood = st.text_input("What mood are you in for reading? (e.g., business, fantasy, mystery)")
    topic = st.text_input("What topic would you like to read about? (e.g., innovation, leadership, AI)")
    style = st.text_input("What writing style do you prefer? (e.g., case study based, narrative, analytical)")

    if st.button("Get Recommendation"):
        if mood and topic and style :
            user_traits = f"{mood}, {topic}, {style}"
            temp(user_traits, book_info, trait_embeddings, category_embeddings)
        else:
            st.warning("Please provide all inputs: mood, topic, style, and categories.")

if __name__ == "__main__":
    main()
