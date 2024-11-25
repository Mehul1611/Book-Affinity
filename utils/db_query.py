QUESTION_ANSWER= """
            INSERT INTO quiz_answers (book_title, question, suggestions, user_answer, created_at)
            VALUES (:book_title, :question, :suggestions, :user_answer, :created_at)
            """

DATA_LOAD="""
            SELECT bt."BookTitle", bt."Traits", b."thumbnail", b."authors", b."description", b."categories" 
            FROM public.book_traits bt
            JOIN public.book b ON bt."BookTitle" = b."title"
            """

FETCH_DATA="""
            SELECT * FROM quiz_answers ORDER BY created_at DESC LIMIT 10
            """

SUMMARY_EXT="""
            SELECT id, title, description FROM {input_table} LIMIT 1000
            """

EMBEDD_INSERT="""
            INSERT INTO cat_embeddings (booktitle, embed_1, embed_2, embed_3) 
            VALUES (%s, %s, %s, %s)
            """

FETCH_EMBEDD="""
            SELECT embed_1, embed_2, embed_3 
            FROM cat_embeddings 
            WHERE booktitle = %s
            """

FETCH_TRAIT="""
            SELECT embed_1, embed_2, embed_3 
            FROM embeddings 
            WHERE booktitle = %s
            """