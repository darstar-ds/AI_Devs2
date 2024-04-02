import requests
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "gpt-4"

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/blogger"
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
    return my_task.json()['msg'], my_task.json()['blog']

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

def prepare_blog_post(chapters):
    blog_texts = []
    for chapter in chapters:
        print(f"Chapter: {chapter}")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": chapter}
                ],
            temperature = 0
            )
        blog_text = response.choices[0].message.content
        print(blog_text)
        blog_texts.append(blog_text)
        # response_json = json.loads(response.model_dump_json())
        # print(response_json)
    return blog_texts

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
my_task_msg, my_task_blog = get_my_task(task_resource_path, parameters)
print(f"My task: {my_task_msg}\nBlog paragraphs: {my_task_blog}")

# Send the answer
blog_texts = prepare_blog_post(my_task_blog)
print(f"Blog texts: {blog_texts}")
answer = {
    "answer": blog_texts
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)