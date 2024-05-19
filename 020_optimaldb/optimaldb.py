"""
Rozwiąż zadanie API o nazwie 'optimaldb'. 
Masz dostarczoną bazę danych o rozmiarze ponad 30kb. 
https://tasks.aidevs.pl/data/3friends.json 
Musisz zoptymalizować ją w taki sposób, aby automat korzystający z niej, 
a mający pojemność pamięci ustawioną na 9kb był w stanie odpowiedzieć 
na 6 losowych pytań na temat trzech osób znajdujących się w bazie. 
Zoptymalizowaną bazę wyślij do endpointa /answer/ jako zwykły string. 
Automat użyje jej jako fragment swojego kontekstu i spróbuje odpowiedzieć na pytania testowe. 
Wyzwanie polega na tym, aby nie zgubić żadnej informacji 
i nie zapomnieć kogo ona dotyczy oraz aby zmieścić się w wyznaczonym limicie rozmiarów bazy.
"""

import requests
import os
import json
from openai import OpenAI
import uuid
import task_ops_framework



my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
my_RENDERFORM_key = os.environ.get("API_RENDERFORM_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "optimaldb"


openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-3.5-turbo"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\020_optimaldb\\"
os.chdir(path)
print(os.getcwd())


def get_database(database):
    try:
        my_task_db_json = requests.get(database).json()
        # print(my_task_db_json)
        try:
            with open("database.json", "w") as f:
                json.dump(my_task_db_json, f)
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP Error: {http_err}')
            raise  
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_task_db_json.content}')  # This will show more details
        raise       
    return my_task_db_json

def get_summary(joined_texts):
    system_content = """
                    Summarize. 
                    Keep the info about favourite movies.
                    Keep the info about dancing.
                    """
    response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"{joined_texts}"}
                ],
        temperature = 0,
        model=CHAT_MODEL,
        # max_tokens=20,
    )
    return response.choices[0].message.content 

def merge_all_facts(my_database):
    all_facts = ""
    for _, statements in my_database.items():
        person_description = "\n".join(statements)
        # print(person_description)
        one_person_summary = get_summary(person_description)
        # print(f"ONE PERSON SUMMARY\n{one_person_summary}")
        all_facts += one_person_summary
        print(f"ALL FACTS:\n{all_facts}")
        with open("summary.txt", "w") as f:
                json.dump(all_facts, f)
    return all_facts   


task_ops_client = task_ops_framework.TaskMainOps()

# Get the token value of the task
my_task_token = task_ops_client.get_token(taskname)

# Get the content of the task and references
my_task_msg = task_ops_client.fetch_task(my_task_token) 

my_database_json = get_database(my_task_msg['database'])
my_facts = merge_all_facts(my_database_json)


# my_task_image = get_image(my_task_image_url, "downloaded_image.png")
# my_task_text = my_task_msg['text']
# print(f"Tekst do mema: {my_task_text}")

# my_meme = render_image(rf_template_id, my_task_image_url, my_task_text)

# Submit answer
answer = my_facts
# print(f"Answer: {answer}\nAnswer type: {type(answer)}")
my_result = task_ops_client.submit_answer(answer, my_task_token)
