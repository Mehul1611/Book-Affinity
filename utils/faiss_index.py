import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

load_dotenv() 


model_name = os.getenv("EMBEDDING_MODEL")
model=SentenceTransformer(model_name)


def initialize_faiss_index(data):
    embedding_dim = model.get_sentence_embedding_dimension()
    index = faiss.IndexFlatIP(embedding_dim)  
    book_info = []
    trait_embeddings = []  
    
    for _, row in data.iterrows():
        book_info.append(row['BookTitle'])  
        embeddings_for_traits = []
        try:
            traits = row['Traits'].split(",")  
            for trait in traits:
                embedding = model.encode(trait.strip()).astype(np.float32)
                embeddings_for_traits.append(embedding)
                index.add(np.array([embedding]))  

            trait_embeddings.append(embeddings_for_traits)  
        except:
            print(_, row['Traits'])
    data["Embeddings"] = trait_embeddings
    return index, book_info, data