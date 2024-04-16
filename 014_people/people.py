import requests
import os
import json
import re
import time
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\014_people\\"
os.chdir(path)
print(os.getcwd())

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/people"
resource_path = str(resource + taskname)

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
qdrant_client = QdrantClient(url="http://localhost:6333")
CHAT_MODEL = "gpt-4"
EMBEDDING_MODEL = "text-embedding-ada-002"


def get_my_token(resource_path, parameters):
    headers = {'Content-Type': 'application/json'} 
    try:
        my_token = requests.post(resource_path, json=parameters, headers=headers)
        my_token.raise_for_status()
        print(f"My token: {my_token}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_token.content}')  # This will show more details
        raise
    return my_token.json()['token']

def get_my_task(task_resource_path, parameters):
    headers = {'Content-Type': 'application/json'} 
    try:
        my_task = requests.get(task_resource_path, json=parameters, headers=headers)
        my_task.raise_for_status()
        print(f"My task: {my_task.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_task.content}')  # This will show more details
        raise
    return my_task.json()['msg'], my_task.json()['data'], my_task.json()['question'], my_task.json()['hint1'], my_task.json()['hint2'] #


def send_my_answer(resource_path, answer):
    headers = {'Content-Type': 'application/json'} 
    try:
        my_answer = requests.post(resource_path, json=answer, headers=headers)
        my_answer.raise_for_status()
        print(f"My result: {my_answer}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_answer.content}')  # This will show more details
        raise
    return my_answer.json()


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


def get_people_data(people_data_url):
    headers = {'Content-Type': 'application/json'} 
    try:
        response = requests.get(people_data_url, headers=headers) #json=answer, 
        response.raise_for_status()
        print(f"My result, top 1: {response.json()[:1]}\nRecords no: {len(response.json())}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {response.content}')  # This will show more details
        raise
    return response.json()


def get_embedding(string):
    response = openai_client.embeddings.create(
        input=[string],
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding


def create_collection_in_qdrant(people_data):
    
    my_collection_name = "people_data"

    if qdrant_client.collection_exists(collection_name=my_collection_name):
        print(f"The collection {my_collection_name} exists.")
        pass
    else:
        print(f"The collection {my_collection_name} does not exist. Let's create one.")
        qdrant_client.create_collection(
            collection_name=my_collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
        #Add records to database
        print("Adding records to qdrant database...")
        new_people_data = []
        for item in people_data: #[:3]
            item_id = str(uuid.uuid4())
            print(f"UUID: {item_id}")
            item['UUID'] = item_id
            print(f"Item: {item}")
            item_content = str(item['imie']) + " " + str(item['nazwisko']) + " " + str(item['wiek']) + " " + str(item['o_mnie']) + " " + str(item['ulubiona_postac_z_kapitana_bomby']) + " " + str(item['ulubiony_serial']) + " " + str(item['ulubiony_film']) + " " + str(item['ulubiony_kolor'])
            print(f"Cały item_content: {item_content}")
            item_vector = get_embedding(item_content)
            print(f"Vector: {item_vector[:3]}")
            print(f"Full URL: {item}")
            new_people_data.append(item)
            print(f"Pełna lista new_people_data: {new_people_data}")
            
            #Upload item to qdrant database
            qdrant_client.upsert(
                collection_name=my_collection_name,
                points=[
                    PointStruct(
                        id=item_id,
                        vector=item_vector,
                        payload=item
                        )
                    ]
                )
        # Dump new_people_data to JSON file
        with open('new_people_data.json', 'w') as outfile:
            json.dump(new_people_data, outfile)
            print("new_people_data.json dumped to disk.")

       
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


parameters = {
    "apikey": my_AIDEVS2_key
    }

# Get the token value of the task
mytask_token = get_my_token(resource_path, parameters)
# print(f"Token value: {mytask_token}")

# Get the content of the task and references
task_resource_path = str(resource + "/task/" + mytask_token)
my_task_msg, my_task_data, my_task_question, my_task_hint1, my_task_hint2 = get_my_task(task_resource_path, parameters) #
print(f"My task: {my_task_msg}\nData: {my_task_data}\nQuestion: {my_task_question}\nHint1: {my_task_hint1}\nHint2: {my_task_hint2}") #

# Get the URLs from a newsletter of "unknown"
people_data_url = "https://tasks.aidevs.pl/data/people.json"
people_data = get_people_data(people_data_url)
# q_keywords = get_q_keywords(my_task_question)
# print(f"Słowa kluczowe w pytaniu: {q_keywords}")

create_collection_in_qdrant(people_data)
my_task_q_vector = get_embedding(my_task_question)
similar_content = find_similar(my_task_q_vector)
task_query_answer = build_answer(similar_content, my_task_question)
print(f"Pytanie: {my_task_question}\nOdpowiedź na pytanie: {task_query_answer}")

answer = {
    "answer": str(task_query_answer)
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)