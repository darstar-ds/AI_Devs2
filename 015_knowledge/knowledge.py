import requests
import os
import json
from openai import OpenAI
import uuid
import country_data
import task_ops_framework
import currencies


my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "knowledge"

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-4"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\015_knowledge\\"
os.chdir(path)
print(os.getcwd())


def find_population(country_name):
    country_info = country_data.CountryInfo(country_name)
    population = country_info.get_country_data()[0]['population']
    print(f"Population: {population}")
    return population

def find_curr_course(my_currency):
    curr_table = currencies.CurrCurrency()
    mid_curr = curr_table.get_curr_rate(my_currency)["rates"][0]["mid"]
    print(mid_curr)
    return mid_curr

def find_q_cat(my_task_question):
    q_cat_system_content = """
        Jesteś specjalistą w rozpoznawaniu kategorii pytań.
        Zastanów się, do jakiej kategorii najlepiej pasuje pytanie użytkownika. 
        Wybierz tylko jedną z trzech kategorii:
        - waluty
        - populacja
        - inne
        Odpowiedź zwróć w formacie JSON, według wzoru.
        WZÓR:
        ###
        {
            "kategoria": "waluty",
            "value": "EUR"
            }
        {
            "kategoria": "populacja",
            "value": "Francja"
            }
        {
            "kategoria": "inne"
            "value": "pytanie"
            }
        ###
            
        Jeśli kategoria to "populacja", znajdź w pytaniu nazwę kraju i podaj jej angielską wersję w polu "value".
        Jeśli kategoria to "waluty", znajdź w pytaniu nazwę waluty i podaj jej trzyliterowy kod w polu "value". Kod ma być zgodny ze standardem ISO 4217.
        Jeśli kategoria to "inne", do pola "value" wstaw pytanie użytkownika.
        """

    response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": q_cat_system_content},
                {"role": "user", "content": my_task_question}
                ],
        temperature = 0,
        model=CHAT_MODEL
    )
    return response.choices[0].message.content

def find_answer(my_task_question):
    q_category = json.loads(find_q_cat(my_task_question)) # ['kategoria']
    print(f"Question category: {q_category}")
    if q_category['kategoria'] == "populacja":
        answer = find_population(q_category['value'])
    elif q_category['kategoria'] == "waluty":
        answer = find_curr_course(q_category['value'])
    else:
        response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": "Odpowiedz na pytanie użytkownika"},
                {"role": "user", "content": my_task_question}
                ],
        temperature = 0,
        model=CHAT_MODEL
        )
        answer = response.choices[0].message.content
    return answer





task_ops_client = task_ops_framework.TaskMainOps()

# Get the token value of the task
my_task_token = task_ops_client.get_token(taskname)

# Get the content of the task and references
my_task_msg = task_ops_client.fetch_task(my_task_token) 
# for key in my_task_msg:
#     print(f"{key}: {my_task_msg[key]}")
my_task_question = my_task_msg['question']
print(f"My task question: {my_task_question}")

# Submit answer
answer = find_answer(my_task_question)
print(f"Answer: {answer}")
my_result = task_ops_client.submit_answer(answer, my_task_token)
