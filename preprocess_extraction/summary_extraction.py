import pandas as pd
from sqlalchemy import text
from book_main.constant import LLM_NAME, CLIENT
from book_main.utils.db_query import SUMMARY_EXT
from book_main.utils.db_utils import database
from llm.prompt import SUMMARY_EXTRACTION


class SummaryExtractor:
    def __init__(self):
        self.engine = database.get_engine()
        self.llm_name = LLM_NAME
        self.client = CLIENT
        self.summary_extraction_prompt = SUMMARY_EXTRACTION

    def generate_summary(self, book_title, description):
        """Generate a summary using the LLM."""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.summary_extraction_prompt.format(
                        book_title=book_title, description=description
                    ),
                },
            ],
            model=self.llm_name,
        )
        return chat_completion.choices[0].message.content.strip()

    def extract_and_store_summaries(self, input_table, output_table):
        with self.engine.connect() as connection:
            query = text(SUMMARY_EXT.format(input_table=input_table))
            books_df = pd.read_sql(query, connection)

            if 'title' not in books_df.columns or 'description' not in books_df.columns:
                raise ValueError("Table must contain 'title' and 'description' columns.")

            results = []

            for index, row in books_df.iterrows():
                book_id = row['id']
                book_title = row['title']
                description = row['description']

                summary = self.generate_summary(book_title, description)
                results.append({'id': book_id, 'BookTitle': book_title, 'Summary': summary})

            results_df = pd.DataFrame(results)
            results_df.to_sql(output_table, connection, if_exists='replace', index=False)
            print(f"Summaries successfully stored in the '{output_table}' table.")


if __name__ == "__main__":
    input_table = "book"
    output_table = "book_summaries"

extractor = SummaryExtractor()
extractor.extract_and_store_summaries(input_table, output_table)
