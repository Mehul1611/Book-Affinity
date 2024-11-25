import numpy as np
from book_main.constant import MODEL, CONNECTION
from book_main.utils.db_query import EMBEDD_INSERT, FETCH_EMBEDD, FETCH_TRAIT
import ast


class EmbeddingManager:
    def __init__(self):
        self.connection = CONNECTION

    def save_embeddings(self, traits, book_title):
        traits_list = [trait.strip() for trait in traits.split(",")]
        embeddings = [
            MODEL.encode(traits_list[0]).astype(np.float32),
            MODEL.encode(traits_list[1]).astype(np.float32) if len(traits_list) > 1 else MODEL.encode(traits_list[0]).astype(np.float32),
            MODEL.encode(traits_list[2]).astype(np.float32) if len(traits_list) > 2 else MODEL.encode(traits_list[0]).astype(np.float32),
        ]
        cursor = self.connection.cursor()
        cursor.execute(EMBEDD_INSERT, (
            book_title, 
            embeddings[0].tolist(),
            embeddings[1].tolist(),
            embeddings[2].tolist(),
        ))
        self.connection.commit()
        cursor.close()


    def fetch_categories(self, book_title):
        cursor = self.connection.cursor()
        cursor.execute(FETCH_EMBEDD, (book_title,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return [np.array(ast.literal_eval(result[i]), dtype=np.float32) for i in range(3)]
        return None

    def fetch_embeddings(self, book_title):
        cursor = self.connection.cursor()
        cursor.execute(FETCH_TRAIT, (book_title,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return [np.array(ast.literal_eval(result[i]), dtype=np.float32) for i in range(3)]
        return None

manager=EmbeddingManager()
