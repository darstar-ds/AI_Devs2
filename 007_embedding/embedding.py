import requests
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "text-embedding-ada-002"

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/embedding"
resource_path = str(resource + taskname)

system_content = """
Jestem mistrzem w robieniu pizzy. 
Potrafię doskonale opisać sposób robienia pizzy. 
Gdy podasz mi temat, to przygotuję Ci akapit tekstu na bloga."
"""

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
    return my_task.json()['msg'], my_task.json()['hint1'], my_task.json()['hint2'], my_task.json()['hint3']

def send_my_answer(resource_path, answer):
    headers = {'Content-Type': 'application/json'} 
    try:
        my_answer = requests.post(resource_path, json=answer, headers=headers)
        my_answer.raise_for_status()
        print(f"My result: {my_answer.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_answer.content}')  # This will show more details
        raise
    return my_answer.json()

def get_embedding(sentence):
    response = client.embeddings.create(
        input=[sentence],
        model=MODEL
    )
    return response.data[0].embedding

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
my_task_msg, my_task_hint1, my_task_hint2, my_task_hint3 = get_my_task(task_resource_path, parameters) #, my_task_blog
print(f"My task: {my_task_msg}\n \
      Hint1: {my_task_hint1}\n \
      Hint2: {my_task_hint2}\n \
      Hint3: {my_task_hint3}") 

# Send the answer
my_embedding = get_embedding("Hawaiian pizza")
print(f"Length of embedding: {len(my_embedding)}")
answer = {
    "answer": my_embedding
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)