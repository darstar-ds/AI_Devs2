import requests
import os
import json

class TaskMainOps:
    def __init__(self):
        self.base_url = "https://tasks.aidevs.pl"
        self.headers = {'Content-Type': 'application/json'}
        self.api_key = {"apikey": os.environ.get("API_AIDEVS2_KEY")}

    def get_token(self, taskname):
        token_resource_path = f"{self.base_url}/token/{taskname}"
        try:
            response = requests.post(token_resource_path, json=self.api_key, headers=self.headers)
            response.raise_for_status()
            # print(f"My token: {response.json()['token']}")
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP Error: {http_err}')
            print(f'Response content: {response.content}')  # This will show more details
            raise
        return response.json()['token']

    def fetch_task(self, my_task_token):
        task_resource_path = f"{self.base_url}/task/{my_task_token}"
        try:
            my_task = requests.get(task_resource_path, json=self.api_key, headers=self.headers)
            my_task.raise_for_status()
            # print(f"My task: {my_task.json()}")
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP Error: {http_err}')
            print(f'Response content: {my_task.content}')  # This will show more details
            raise
        return my_task.json()

    def submit_answer(self, answer, my_task_token):
        answer_json = {"answer": answer}
        answer_resource_path = f"{self.base_url}/answer/{my_task_token}"
        try:
            is_correct = requests.post(answer_resource_path, json=answer_json, headers=self.headers)
            is_correct.raise_for_status()
            print(f"My result: {is_correct}")
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP Error: {http_err}')
            print(f'Response content: {is_correct.content}')  # This will show more details
            raise
        return is_correct.json()

