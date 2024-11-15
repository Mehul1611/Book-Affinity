QUESTION_PROMPT='''Generate exactly 10 thought-provoking questions for the book titled ‘{book_title}’ that present hypothetical scenarios or alternative viewpoints on the characters’ actions, motives, or relationships.
Each question should subtly encourage readers to consider different facets of the characters’ personalities and decisions without revealing that their own perceptions are being evaluated. 
Avoid direct language that might make it obvious to the reader that their perception is being assessed; instead, frame each question as a natural part of exploring character development and story depth.
For each question, provide exactly 3 nuanced answer choices that align with possible interpretations or responses, varying subtly in perspective. If the book or characters are not found, respond with ‘Not Found.
'''

SUMMARY_PROMPT='''
Provide a brief summary of the book titled "{book_title}".
If the title resembles some character of some book then consider it.
If the book is not found, respond with 'Not Found'.
'''

RECOMMENDATION_PROMPT='''
You are a helpful assistant that extract 3 most prominent traits based on the user's mood, topic, and writing style preferences.
The user provides the following information:
- Mood: {mood}
- Topic: {topic}
- Writing Style: {style}
** Format the output as a comma-separated string without any descriptions or additional information.
'''
PER_TRAITS_PROMPT = '''
Analyze the user's responses to a set of questions related to the book titled '{book_title}'. Each question and its corresponding answer is provided below:
Questions: {questions}
 and Answers:
{user_answers}
For each answer, identify the personality traits that best correspond to the user's choices. Focus on extracting traits that dynamically reflect the user's reasoning, preferences, and thought process. Ensure that each question-answer pair uniquely contributes to the overall personality assessment.

**Output a comma-separated list of the top three traits that most prominently represent the user's personality, derived from their responses to these questions. Do not include any descriptions, explanations, or additional formatting in the output.**
'''
TRAIT_PROMPT = """
Read the following summary and extract the top 3 personality traits that are most relevant:
Summary: {summary}

Return only the names of the traits, separated by commas.
"""