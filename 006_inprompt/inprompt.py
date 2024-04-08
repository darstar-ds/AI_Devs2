import requests
import os
import json
from openai import OpenAI


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\006_inprompt"
os.chdir(path)
print(os.getcwd())

client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "gpt-4"

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/inprompt"
resource_path = str(resource + taskname)

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
        # print(f"My task: {my_task.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_task.content}')  # This will show more details
        raise
    return my_task.json()['msg'], my_task.json()['input'], my_task.json()['question']

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


def find_name_in_question(my_task_question):
    system_content = """
        Znajdź imię w podanym pytaniu. Jako odpowiedź podaj samo imię, nic więcej.
        """

    response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": my_task_question}
                ],
            temperature = 0
            )
    only_name = response.choices[0].message.content
    print(only_name)
    return only_name

def find_description_in_input(my_task_input, only_name):
    useful_sentences = []
    for item in my_task_input:
        if only_name in item:
            useful_sentences.append(item)
    
    print(f"Useful sentences: {useful_sentences}")
    return useful_sentences

def let_LLM_answer(my_task_question, useful_sentences):
    system_content = f"""
            Wykorzystaj podany niżej kontekst, aby odpowiedzieć na zadane pytanie. 
            Odpowiadaj możliwie zwięźle. 
            Maksymalnie w dwóch zdaniach.
            Jeśli w kontekście brak informacji, odpowiedz "Nie wiem".

            Kontekst:
            ###{useful_sentences}###
        """
    
    response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": my_task_question}
                ],
            temperature = 0
            )
    LLM_answer = response.choices[0].message.content
    print(LLM_answer)
    return LLM_answer

parameters = {
    "apikey": my_AIDEVS2_key
    }

# print(f"My API key: {my_AIDEVS2_key}")
# print(f"Resource path: {resource_path}")
# print(parameters)

# Get the token value of the task
mytask_token = get_my_token(resource_path, parameters)
print(f"Token value: {mytask_token}")

# Get the content of the task and references
task_resource_path = str(resource + "/task/" + mytask_token)
my_task_msg, my_task_input, my_task_question = get_my_task(task_resource_path, parameters)

# print(f"Input: {my_task_input}")
print(f"Question: {my_task_question}")

# Open the file in write mode
with open("input.txt", "w", encoding="utf-8") as f:
    for item in my_task_input:
        # print(f"Item: {item}")
        f.write(str(item) + "\n")

only_name = find_name_in_question(my_task_question)
useful_sentences = find_description_in_input(my_task_input, only_name)
answer4name = let_LLM_answer(my_task_question, useful_sentences)

# Send the answer

answer = {
    "answer": answer4name
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)