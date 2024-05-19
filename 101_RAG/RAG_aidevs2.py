import os
import numpy as np
from openai import OpenAI
import mds_converter
import embedder
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

chunks_path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\_AI_Devs2_teksty\\"

# Convert MD files into chunks and save as txt files
md_converter = mds_converter.MD_Converter(mds_path)
md_converter.mds_converter()


# chunks = [["Ciekawe, czy to ma znaczenie, jak pytanie jest po polsku?"],
#           ["Jak zainstalować Dockera i Qdranta?"]
#           ]

txt2embeddings = embedder.embedder(chunks_path)
# txt_embeddings = txt2embeddings.get_embedding_from_hf(chunks)
# text_embeddings = np.array([txt2embeddings.get_embedding_from_hf(chunk) for chunk in chunks])

#Create ds_qdrant class with path to txt files/chunks, collection name, embedder name and vectr length
#embedder name = "hf_embedder" OR "mistral_embedder" OR "st_embedder"
#vector legth = hf/384 OR mistral/1024 OR st/768
txt_as_vector2qdrant = qdrant_ops.ds_qdrant(
    chunks_path, 
    embedder_name = "st_embedder", 
    my_collection_name = "AIDEVS2",
    vector_length = 768
    )
txt_as_vector2qdrant.create_collection_in_qdrant()
txt_as_vector2qdrant.add_vectors_2_collection()

# for chunk in chunks:
    # txt2embeddings.get_embedding_from_hf(chunk)
    # txt2embeddings.get_embedding_from_mistral(chunk)
    # txt2embeddings.get_embedding_from_st(chunk)

# create_collection_in_qdrant(people_data)
# my_task_q_vector = get_embedding(my_task_question)
# similar_content = find_similar(my_task_q_vector)
# task_query_answer = build_answer(similar_content, my_task_question)
# print(f"Pytanie: {my_task_question}\nOdpowiedź na pytanie: {task_query_answer}")


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




       
def find_similar(my_task_q_vector):
    query_results = qdrant_client.search(
        collection_name = "people_data",
        query_vector = my_task_q_vector,
        limit = 5
        )          
    print(query_results)
    primo_score_payload = query_results[0].payload
    print(f"Length: {len(query_results)}")
    # print(f"Primo score payload: {primo_score_payload}")
    formated_data = []
    for i in range(0, len(query_results)):
        # formated_scorepoint = "imie i nazwisko" + " " + query_results[i].payload['imie'] + " " +\
        #     query_results[i].payload['nazwisko'] + " " +\
        #     "wiek:" + " " +query_results[i].payload['wiek'] + " " +\
        #     query_results[i].payload['o_mnie'] + " " +\
        #     query_results[i].payload['ulubiona_postac_z_kapitana_bomby'] + " " +\
        #     query_results[i].payload['ulubiony_film'] + " " +\
        #     query_results[i].payload['ulubiony_serial'] + " " +\
        #     query_results[i].payload['ulubiony_kolor'] + " " +\
        
        
        formated_data.append(query_results[i].payload)

    print(formated_data)

    return formated_data


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
