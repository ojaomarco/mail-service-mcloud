import requests
from config.auth import BASE_URL, AUTH

class Client:
    def __init__(self):
        self.url = f'{BASE_URL}'
    
    def get_all_devices(self):
        data_list = []
        response = requests.get(self.url, auth=AUTH)
        data = response.json()
        for x in response.json()['results']: data_list.append(x) 

        while data['next'] is not None:
            print("Next page found, downloading", data['next'])
            response = requests.get(data['next'], auth=AUTH)
            data = response.json()
            for x in response.json()['results']: data_list.append(x) 

        return(data_list)
    
    def get_all_users(self):
        data_list = []
        response = requests.get('http://multipetcloud.com.br/api/users', auth=AUTH)
        data = response.json()
        data_list.append(response.json()['results'])
        while data['next'] is not None:
           print("Next page found, downloading", data['next'])
           response = requests.get(data['next'], auth=AUTH)
           data = response.json()
           data_list.append(data['results'])
        return data_list
        
if __name__ == '__main__':
    client = Client('aa')
    client.get_data()
"""
    {
         "id":"7256eb75-f438-46dc-b364-93b97aeecd78",
         "name":"Maq México 8000",
         "description":"8000 México",
         "status":3,
         "is_running":0,
         "serial_number":"025.075.09-23",
         "node":{
            "company":{
               "id":"aa158aad-bd50-43db-a585-2e912a12f7da",
               "name":"Multipet",
            }
         },
         "model":{     
            "name":"Sopradora Multipet 8.000",
         }
      }"""