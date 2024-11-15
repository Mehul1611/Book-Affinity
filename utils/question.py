from groq import Groq
from book_main.app.config.template import QUESTION_PROMPT, SUMMARY_PROMPT
import os
from dotenv import load_dotenv


load_dotenv()
API1=os.getenv("API1")
api_key = API1
client = Groq(api_key=api_key)

def generate_summary(book_title):    
    query = SUMMARY_PROMPT.format(book_title=book_title)
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": query}],
        model="llama3-groq-70b-8192-tool-use-preview",
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
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    try:
        response_content = response.choices[0].message.content.strip()
        if "Not Found" in response_content:
            return None
        return response_content.split("\n\n")  # Return questions as a list
    except (IndexError, AttributeError):
        return None