from collections import defaultdict
import requests
from datetime import datetime, timedelta
from config.auth import BASE_URL, AUTH, BASE_URL_ISSUE

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

    def get_all_issues(self):
        final_time = datetime.now().isoformat()
        initial_time = (datetime.now()-timedelta(hours=24)).isoformat()
        response = requests.get(f'{BASE_URL_ISSUE}?time_from={initial_time}Z&time_to={final_time}Z&limit=-1', auth=AUTH)
        data = response.json()
        issues_by_device = defaultdict(list)
        for issue in data:
            issues_by_device[issue["device"]].append(issue)
        return issues_by_device
    