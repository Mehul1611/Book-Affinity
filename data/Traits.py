import requests
import time
from sqlalchemy import Table, MetaData, select, insert
from book.app.config.template import TRAIT_PROMPT
from book.app.database.config import get_engine

groq_api_url = 'https://api.groq.com/openai/v1/chat/completions'

import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm_model_name = os.getenv("LLM_MODEL_NAME")

def extract_traits(summary):
    prompt = TRAIT_PROMPT.format(summary=summary)

    payload = {
        "model": llm_model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }
    
    headers = {
        'Authorization': f'Bearer {groq_api_key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(groq_api_url, json=payload, headers=headers)

    if response.status_code == 200:
        content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        traits = content.strip()
        print(f"Extracted Traits: {traits}")
        return traits
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Error"

def clean_traits(traits_output):
    if traits_output == "Error":
        return ""
    
    traits_list = [trait.strip() for trait in traits_output.replace('\n', ',').split(',') if trait.strip()]
    return ", ".join(traits_list)

def process_traits():
    engine = get_engine()
    metadata = MetaData(bind=engine)
    
    book_table = Table('book_summaries', metadata, autoload_with=engine)
    book_sum_table = Table('book_traits', metadata, autoload_with=engine)
    
    with engine.connect() as conn:
        query = select([book_table.c.id, book_table.c.summary])
        results = conn.execute(query).fetchall()
    
        extracted_traits = []
        cleaned_traits = []
    
        for row in results:
            book_id, summary = row
            raw_traits = extract_traits(summary)
            extracted_traits.append(raw_traits)
            cleaned = clean_traits(raw_traits)
            cleaned_traits.append(cleaned)

            insert_stmt = insert(book_sum_table).values(
                book_id=book_id,
                extracted_traits=raw_traits,
                cleaned_traits=cleaned
            ).on_conflict_do_update(
                index_elements=['book_id'],
                set_=dict(extracted_traits=raw_traits, cleaned_traits=cleaned)
            )
            with engine.begin() as trans_conn:
                trans_conn.execute(insert_stmt)
    
    print("Trait extraction complete. Results saved to the database.")

if __name__ == "__main__":
    process_traits()