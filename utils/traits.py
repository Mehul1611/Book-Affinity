
import streamlit as st
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from book_main.app.config.template import PER_TRAITS_PROMPT
from book_main.app.database.config import get_engine , load_data_from_db, fetch_last_entries
from book_main.app.utils.faiss_index import initialize_faiss_index
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API1=os.getenv("API1")
model_name=os.getenv("EMBEDDING_MODEL")
model=SentenceTransformer(model_name)
llm_name=os.getenv("LLM_MODEL_NAME")
data = load_data_from_db() 
index, book_info, data = initialize_faiss_index(data)


def PerTra():
    df = fetch_last_entries()
    if df.empty:
        st.warning("No recent entries found in the database.")
        return None

    user_answers = df['user_answer'].tolist()
    book_title = df['book_title'].iloc[0]  
    questions=df['question']
    analysis_prompt = PER_TRAITS_PROMPT.format(book_title=book_title, user_answers=user_answers, questions=questions)

    def call_groq_api(prompt):
        url = 'https://api.groq.com/openai/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {API1}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': llm_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150,
            'temperature': 0.7
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            traits_summary_text = response.json()['choices'][0]['message']['content']
            traits_summary = traits_summary_text.split(", ")
            return traits_summary
        else:
            st.error(f"Groq API Error: {response.status_code} - {response.text}")
            return None

    traits_summary = call_groq_api(analysis_prompt)
    return traits_summary



def temp(user_traits):
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
