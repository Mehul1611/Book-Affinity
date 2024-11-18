from groq import Groq
from book.app.config.template import QUESTION_PROMPT, SUMMARY_PROMPT
import os
from dotenv import load_dotenv


load_dotenv()
API1=os.getenv("GROQ_API_KEY")
api_key = API1
client = Groq(api_key=api_key)
llm_model_name = os.getenv("LLM_MODEL_NAME")

def generate_summary(book_title):    
    query = SUMMARY_PROMPT.format(book_title=book_title)
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": query}],
        model=llm_model_name,
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

    response = client.chat.completions.create(
        messages=[{"role": "system", "content": query}],
        model=llm_model_name,
    )
    try:
        response_content = response.choices[0].message.content.strip()
        if "Not Found" in response_content:
            return None
        return response_content.split("\n\n")  
    except (IndexError, AttributeError):
        return None