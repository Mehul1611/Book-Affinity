import streamlit as st
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from book_main.app.database.config import get_engine  , load_data_from_db
from book_main.app.utils.faiss_index import initialize_faiss_index
from book_main.app.config.template import RECOMMENDATION_PROMPT  
import os
import requests
import requests
from dotenv import load_dotenv

load_dotenv()
API1=os.getenv("API1")
model_name=os.getenv("EMBEDDING_MODEL")
llm_name=os.getenv("LLM_MODEL_NAME")
model = SentenceTransformer(model_name)



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
        recommendations = response.json()['choices'][0]['message']['content']
        return recommendations.split("\n")  
    else:
        print("Error:", response.status_code, response.text)
        return []



def temp(user_traits, data):
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


data = load_data_from_db()  
index, book_info, data = initialize_faiss_index(data)


def main():
    st.title("Personalized Book Recommendation System")
    st.subheader("Tell us your reading preferences")
    mood = st.text_input("What mood are you in for reading? (e.g., business, fantasy, mystery)")
    topic = st.text_input("What topic would you like to read about? (e.g., innovation, leadership, AI)")
    style = st.text_input("What writing style do you prefer? (e.g., case study based, narrative, analytical)")
    if st.button("Get Recommendation"):
        if mood and topic and style:
            user_prompt = f"I am in a mood for reading a {mood} book about {topic} that has a {style} writing style."
            user_prompt = RECOMMENDATION_PROMPT.format(mood=mood, topic=topic, style=style)
            recommendations = call_groq_api(user_prompt)
            recommendations=", ".join(recommendations)
            temp(recommendations, data)
        else:
            st.warning("Please provide all inputs: mood, topic, and style.")

if __name__ == "__main__":
    main()
