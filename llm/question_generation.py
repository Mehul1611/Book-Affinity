from book_main.llm.prompt import QUESTION_PROMPT, SUMMARY_PROMPT
import streamlit as st
import requests
from book_main.constant import GROQ_API_KEY, GROQ_URL, LLM_NAME, CLIENT

def call_groq_api(prompt):
        url = GROQ_URL
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': LLM_NAME,
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
        
def generate_summary(book_title):    
    query = SUMMARY_PROMPT.format(book_title=book_title)
    response = CLIENT.chat.completions.create(
        messages=[{"role": "system", "content": query}],
        model=LLM_NAME,
    )

    try:
        response_content = response.choices[0].message.content.strip()
        if "Not Found" in response_content:
            return None
        return response_content
    except (IndexError, AttributeError):
        return None


def generate_questions(book_title):
    query = QUESTION_PROMPT.format(book_title=book_title)

    response = CLIENT.chat.completions.create(
        messages=[{"role": "system", "content": query}],
        model=LLM_NAME,
    )
    try:
        response_content = response.choices[0].message.content.strip()
        if "Not Found" in response_content:
            return None
        return response_content.split("\n\n")  
    except (IndexError, AttributeError):
        return None