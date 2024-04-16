import requests

class CurrCurrency:
    def __init__(self):
        self.base_url = "http://api.nbp.pl/api/exchangerates/rates/a/"
    
    def get_curr_rate(self, my_currency):
        curr_code = my_currency
        resource_path = f"{self.base_url}{curr_code}"
        headers = {'Content-Type': 'application/json'} 
        try:
            response = requests.get(resource_path, headers=headers)
            response.raise_for_status()
            print(f"My response: {response}")
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP Error: {http_err}')
            print(f'Response content: {response.content}')
            raise
        return response.json()
    
