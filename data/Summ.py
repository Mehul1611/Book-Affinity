from groq import Groq
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

API1 = os.getenv("GROQ_API_KEY")
llm_name = os.getenv("LLM_MODEL_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")  

client = Groq(api_key=API1)


engine = create_engine(DATABASE_URL)

def generate(book_title, description):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Generate a summary for book title: {book_title}. Description: {description}"
            },
        ],
        model=llm_name,
    )
    return chat_completion.choices[0].message.content.strip()

def extract_summaries_from_db(input_table, output_table):
    with engine.connect() as connection:
        query = text(f"SELECT id, title, description FROM {input_table} LIMIT 1000;")
        books_df = pd.read_sql(query, connection)


        if 'title' not in books_df.columns or 'description' not in books_df.columns:
            raise ValueError("Table must contain 'title' and 'description' columns.")

        results = []

        for index, row in books_df.iterrows():
            book_id = row['id']
            book_title = row['title']
            description = row['description']

            summary = generate(book_title, description)
            results.append({'id': book_id, 'BookTitle': book_title, 'Summary': summary})

        results_df = pd.DataFrame(results)
        results_df.to_sql(output_table, connection, if_exists='replace', index=False)
        print(f"Summaries successfully stored in the '{output_table}' table.")


input_table = "book"          
output_table = "book_summaries"  
extract_summaries_from_db(input_table, output_table)