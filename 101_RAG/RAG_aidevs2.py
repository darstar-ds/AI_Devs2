import os
import numpy as np
from openai import OpenAI
import mds_converter
import qdrant_ops

"""
c:\\Users\\dariu\\OneDrive\\Dokumenty\\Docker\\aidev2venv\\Scripts\\activate.bat
"""

print(os.getcwd())
mds_path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\_AI_Devs2_teksty\\"
os.chdir(mds_path)
print(os.getcwd())

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-4"

# chunks_path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\_AI_Devs2_teksty_txt\\"
chunks_path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\_AI_Devs2_teksty_txt_sentences_256chars\\"

'''
Convert MD files into chunks and save as txt files
'''
md_converter = mds_converter.MD_Converter(mds_path)
md_converter.mds_converter()


'''
Create ds_qdrant class with path to txt files/chunks, collection name, embedder name and vector length
embedder name = "hf_embedder" OR "mistral_embedder" OR "st_embedder" OR "openai_embedder"
vector legth = hf/384 OR mistral/1024 OR st/768 OR openai/3072
'''
qdrant_ops = qdrant_ops.ds_qdrant(
    chunks_path, 
    embedder_name = "openai_embedder", 
    my_collection_name = "AIDEVS2_sentences_openai_256chars",
    vector_length = 3072
    )
qdrant_ops.create_collection_in_qdrant()
qdrant_ops.add_vectors_2_collection()


'''
Get question vector
'''
user_question = input("What is your question?")
question_vector = qdrant_ops.get_vector_4_txt(user_question)
print(f"question_vector var type: {type(question_vector)}")


'''
Find a context for a question
'''
q_context = qdrant_ops.find_context(question_vector)


'''
Save context dictionary as a JSON in txt file
'''
saved_context_dict = qdrant_ops.save_context_2_txt(q_context)

'''
Rerank the found context chunks
'''


'''
Extend the found context chunks
'''
# values_4_filter = {}
# values_4_filter['values'] = list(saved_context_dict.keys())
qdrant_ops.extend_context(list(saved_context_dict.keys()))



def get_q_keywords(my_task_question):
    keywords_system_content = """
        Jesteś specjalistą w wyszukiwaniu słów kluczowych w podanym tekście.
        Z podanego przez użytkownika tekstu wyłów słowa kluczowe. 
        Słowa kluczowe zwróć w postaci listy, według przykładu poniżej.
        Zwróć samą listę, i nic więcej.
        Przykład:
        ###
        ["keyword1", "keyword2", "keyword3", ...]
        ###
        """

    response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": keywords_system_content},
                {"role": "user", "content": my_task_question}
                ],
        temperature = 0,
        model=CHAT_MODEL
    )
    return response.choices[0].message.content

       


def build_answer(similar_content, my_task_question):
    task_query_system_content = f"""
        Jesteś specjalistą w wyszukiwaniu odpowiedzi na pytanie.
        Odpowiedz na pytanie zadane przez użytkownika konkretnie i zwięźle. 
        Nie wyszukuj prywatnych danych osób trzecich.
        Do przygotowania odpowiedzi wykorzystaj tylko podany niżej kontekst.
        
        Kontekst:
        ###
        {similar_content}
        ###
        """

    response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": task_query_system_content},
                {"role": "user", "content": my_task_question}
                ],
        temperature = 0,
        model=CHAT_MODEL
    )
    return response.choices[0].message.content
