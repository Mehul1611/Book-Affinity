import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from book.app.database.config import get_engine 
from dotenv import load_dotenv
from sqlalchemy import text
import os
import pickle

load_dotenv() 


model_name = os.getenv("EMBEDDING_MODEL")
model=SentenceTransformer(model_name)

def fetch_data_for_faiss():
    engine=get_engine()
    fetch_sql = "SELECT BookTitle, Trait_Embeddings, Category_Embeddings FROM book_embeddings"
    with engine.connect() as connection:
        result = connection.execute(text(fetch_sql))
        rows = result.fetchall()
    
    book_info = []
    trait_embeddings = []
    category_embeddings = []

    for row in rows:
        book_info.append(row['BookTitle'])

        trait_embeddings.append(pickle.loads(row['Trait_Embeddings']))
        category_embeddings.append(pickle.loads(row['Category_Embeddings']))
    
    return book_info, trait_embeddings, category_embeddings
    


def insert_embeddings(data, model):
    engine=get_engine()
    insert_sql = """
    INSERT INTO book_embeddings (BookTitle, Traits, Categories, Trait_Embeddings, Category_Embeddings)
    VALUES (:BookTitle, :Traits, :Categories, :Trait_Embeddings, :Category_Embeddings)
    ON CONFLICT (BookTitle) DO NOTHING;
    """
    to_insert = []
    for _, row in data.iterrows():
        traits = row['Traits'].split(",") if pd.notna(row['Traits']) else []
        categories = row['categories'].split(",") if pd.notna(row['categories']) else []
     
        trait_embeddings = [model.encode(trait.strip()).astype(np.float32) for trait in traits]
        category_embeddings = [model.encode(category.strip()).astype(np.float32) for category in categories]

        serialized_traits = pickle.dumps(trait_embeddings)
        serialized_categories = pickle.dumps(category_embeddings)
        
 
        to_insert.append({
            "BookTitle": row['BookTitle'],
            "Traits": row['Traits'],
            "Categories": row['categories'],
            "Trait_Embeddings": serialized_traits,
            "Category_Embeddings": serialized_categories
        })
 
    with engine.connect() as connection:
        for entry in to_insert:
            connection.execute(text(insert_sql), entry)
            connection.commit()
    print("Data inserted into 'book_embeddings'.")

