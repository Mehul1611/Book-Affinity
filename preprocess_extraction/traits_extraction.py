import requests
from sqlalchemy import Table, MetaData, select, insert
from book_main.llm.prompt import TRAIT_PROMPT
from book_main.utils.db_utils import database
from book_main.constant import GROQ_API_KEY, GROQ_URL, LLM_NAME


class TraitProcessor:
    def __init__(self):
        self.engine = database.get_engine()
        self.metadata = MetaData(bind=self.engine)
        self.book_table = Table('book_summaries', self.metadata, autoload_with=self.engine)
        self.book_sum_table = Table('book_traits', self.metadata, autoload_with=self.engine)

    def extract_traits(self, summary):
        """Send a summary to the LLM API and extract traits."""
        prompt = TRAIT_PROMPT.format(summary=summary)

        payload = {
            "model": LLM_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300
        }
        
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(GROQ_URL, json=payload, headers=headers)

        if response.status_code == 200:
            content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            traits = content.strip()
            print(f"Extracted Traits: {traits}")
            return traits
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "Error"

    def clean_traits(self, traits_output):
        """Clean and format the raw traits output."""
        if traits_output == "Error":
            return ""
        
        traits_list = [trait.strip() for trait in traits_output.replace('\n', ',').split(',') if trait.strip()]
        return ", ".join(traits_list)

    def process_traits(self):
        """Extract and clean traits for all books in the database and save results."""
        with self.engine.connect() as conn:
            query = select([self.book_table.c.id, self.book_table.c.summary])
            results = conn.execute(query).fetchall()
        
        for row in results:
            book_id, summary = row
            raw_traits = self.extract_traits(summary)
            cleaned = self.clean_traits(raw_traits)

            # Prepare an upsert statement
            insert_stmt = insert(self.book_sum_table).values(
                book_id=book_id,
                extracted_traits=raw_traits,
                cleaned_traits=cleaned
            ).on_conflict_do_update(
                index_elements=['book_id'],
                set_=dict(extracted_traits=raw_traits, cleaned_traits=cleaned)
            )

            with self.engine.begin() as trans_conn:
                trans_conn.execute(insert_stmt)
        
        print("Trait extraction complete. Results saved to the database.")


if __name__ == "__main__":
    processor = TraitProcessor()
    processor.process_traits()
