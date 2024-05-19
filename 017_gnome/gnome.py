"""
Rozwiąż zadanie API o nazwie 'gnome'. 
Backend będzie zwracał Ci linka do obrazków przedstawiających gnomy/skrzaty. 
Twoim zadaniem jest przygotowanie systemu, który będzie rozpoznawał, 
jakiego koloru czapkę ma wygenerowana postać. 
Uwaga! Adres URL zmienia się po każdym pobraniu zadania 
i nie wszystkie podawane obrazki zawierają zdjęcie postaci w czapce. 
Jeśli natkniesz się na coś, co nie jest skrzatem/gnomem, 
odpowiedz “error”. Do tego zadania musisz użyć GPT-4V (Vision).
"""

import requests
import os
import json
from openai import OpenAI
import uuid
import task_ops_framework



my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "gnome"

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-4-turbo"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\017_gnome\\"
os.chdir(path)
print(os.getcwd())


def get_image(url):
    image = requests.get(url)
    if image.status_code == 200:
        # Open the file for writing in binary mode
        with open('downloaded_image.png', 'wb') as file:
            file.write(image.content)
        print("The PNG file has been saved as 'downloaded_image.png'.")
    else:
        print(f"Failed to retrieve the image. Status code: {image.status_code}")
    return image

def describe_image(my_image_url):
    image_system_content = """
        Jesteś specjalistą w rozpoznawaniu zawartości obrazków.
        Przeanalizuj dokładnie zawartość obrazka.
        Jeśli użytkownik zapyta o kolor, podaj tylko kolor w języku polskim i nic więcej.
        Jeśli nie będziesz znał odpowiedzi, powiedz "Error".
        """

    response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": image_system_content},
                {"role": "user", "content": [
                                    {"type": "text", "text": "Jaki jest kolor czapki krasnala?"},
                                    {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"{my_image_url}",
                                    },
                                    },
                                ],
                                }
                ],
        temperature = 0,
        model=CHAT_MODEL,
        max_tokens=20,
    )
    return response.choices[0].message.content



task_ops_client = task_ops_framework.TaskMainOps()

# Get the token value of the task
my_task_token = task_ops_client.get_token(taskname)

# Get the content of the task and references
my_task_msg = task_ops_client.fetch_task(my_task_token) 

my_task_image_url = my_task_msg['url']

my_task_image = get_image(my_task_image_url)

# Submit answer
answer = describe_image(my_task_image_url)
print(f"Answer: {answer}\nAnswer type: {type(answer)}")
my_result = task_ops_client.submit_answer(answer, my_task_token)
