import requests
import os
import json
from openai import OpenAI

print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\008_whisper\\"
os.chdir(path)
print(os.getcwd())
mp3 = path + "mateusz.mp3"

client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "whisper-1"

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/whisper"
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
    return my_task.json()['msg'] #, my_task.json()['hint1'], my_task.json()['hint2'], my_task.json()['hint3']

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

def get_transcription(mp3):
    
    audio_file = open(mp3, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="verbose_json",
        timestamp_granularities=["segment"]
        )
    print(transcription)

    return transcription

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
my_task_msg = get_my_task(task_resource_path, parameters) #, my_task_hint1, my_task_hint2, my_task_hint3
print(f"My task: {my_task_msg}")

# Send the answer
my_transcription = get_transcription(mp3)
# print(f"Length of embedding: {len(my_embedding)}")
# answer = {
#     "answer": my_transcription
#     }

# answer_resource_path = str(resource + "/answer/" + mytask_token)
# accomplish = send_my_answer(answer_resource_path, answer)