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
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\013_search\\"
os.chdir(path)
print(os.getcwd())

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/search"
resource_path = str(resource + taskname)

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "text-embedding-ada-002"


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
    return my_task.json()['msg'], my_task.json()['question'] #, my_task.json()['hint'], my_task.json()['input']


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

def get_embedding(sentence):
    response = openai_client.embeddings.create(
        input=[sentence],
        model=MODEL
    )
    return response.data[0].embedding

def get_URLs_from_unknown(URL):
    headers = {'Content-Type': 'application/json'} 
    try:
        response = requests.get(URL, headers=headers) #json=answer, 
        response.raise_for_status()
        # unkown_URLs = json.loads(response)
        # print(f"My result, first 1: {response.json()[:1]}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {response.content}')  # This will show more details
        raise
    return response.json()

def create_collection_in_qdrant(URLs, my_task_question):
    qdrant_client = QdrantClient(url="http://localhost:6333")
    
    if qdrant_client.collection_exists(collection_name="unknown_URLs"):
        print("The collection 'unknown_URLs' exists.")
        pass
    else:
        print("The collection 'unknown_URLs' does not exist. Let's create one.")
        qdrant_client.create_collection(
            collection_name="unknown_URLs",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
    
    new_URLs = []    
    for URL in URLs: #[:3]
        URL_id = str(uuid.uuid4())
        print(f"UUID: {URL_id}")
        URL['UUID'] = URL_id
        print(f"info: {URL['info']}")
        info_vector = get_embedding(URL['info'])
        print(f"Vector: {info_vector[:3]}")
        print(f"Full URL: {URL}")
        new_URLs.append(URL)
        print(f"Pełna lista new_URLs: {new_URLs}")
        qdrant_client.upsert(
            collection_name="unknown_URLs",
            points=[
                PointStruct(
                    id=URL_id,
                    vector=info_vector,
                    )
                ]
            )

    my_task_q_vector = get_embedding(my_task_question)

    query_results = qdrant_client.search(
        collection_name = "unknown_URLs",
        query_vector = my_task_q_vector,
        limit = 3
        )          
    print(query_results)
    primo_score_id = query_results[0].id
    print(f"Primo score: {primo_score_id}")

    print(f"UUID pierwszego elementu nowych URLi: {new_URLs[0]['UUID']}")
    print(f"Wszystkie nowe URLe: {new_URLs[:5]}")
    for new_URL in new_URLs:
        if new_URL['UUID'] == primo_score_id:
            URL_match = new_URL['url']
    print(f"URL_match {URL_match}")
    return URL_match

parameters = {
    "apikey": my_AIDEVS2_key
    }

# print(f"My API key: {my_AIDEVS2_key}")
# print(f"Resource path: {resource_path}")
# print(parameters)

# Get the token value of the task
mytask_token = get_my_token(resource_path, parameters)
# print(f"Token value: {mytask_token}")

# Get the content of the task and references
task_resource_path = str(resource + "/task/" + mytask_token)
my_task_msg, my_task_question = get_my_task(task_resource_path, parameters) #, my_task_hint, my_task_input, my_task_question, my_task_hint1, my_task_hint2, my_task_hint3
print(f"My task: {my_task_msg}\nQuestion: {my_task_question}") #\nHint: {my_task_hint}, \nInput: {my_task_input}

# Get the URLs from a newsletter of "unknown"
unknown_path = "https://unknow.news/archiwum_aidevs.json"
URLs = get_URLs_from_unknown(unknown_path)
print(f"First URL: {URLs[:1]}")

URL_match = create_collection_in_qdrant(URLs, my_task_question)

answer = {
    "answer": str(URL_match)
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)