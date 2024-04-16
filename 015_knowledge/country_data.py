import requests

class CountryInfo:
    def __init__(self, country_name):
        self.base_url = "https://restcountries.com/v3.1/name/"
        self.country_name = country_name
    
    def get_country_data(self):
        resource_path = self.base_url + self.country_name
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