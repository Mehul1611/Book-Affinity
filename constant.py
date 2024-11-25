import os
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CLIENT = Groq(api_key=GROQ_API_KEY)
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'
LLM_NAME= os.getenv("LLM_MODEL_NAME")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 
CONNECTION=psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}")

MODEL_NAME= os.getenv("EMBEDDING_MODEL")
MODEL=SentenceTransformer(MODEL_NAME)