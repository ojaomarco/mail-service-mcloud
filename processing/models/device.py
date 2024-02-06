import requests
import json 
from config.auth import BASE_URL, AUTH
AUTH =('ojaomarco', 'Jo@o1501')
class Device:
   def __init__(self, data):
      self.id_device = data['id']
      self.name_device = data['name']
      self.description = data['description']
      self.status = data['status']
      self.is_running = data['is_running']
      self.serial_number = data['serial_number']
      self.id_company = data['node']['company']['id']
      self.name_company = data['node']['company']['name']
      self.model = data['model']['name']
        
   def _get_company_users(self, data_list):
      # data_list = []
      users_info = []

      '''response = requests.get('http://multipetcloud.com.br/api/users', auth=AUTH)
      data = response.json()
      data_list.append(response.json()['results'])
      while data['next'] is not None:
         print("Next page found, downloading", data['next'])
         response = requests.get(data['next'], auth=AUTH)
         data = response.json()
         data_list.append(data['results'])'''
      
      for users in data_list:
         for user in users:
            if user.get("company", {}).get("id") == self.id_company:
                user_info = {"id": user["id"], "email": user["email"]}
                users_info.append(user_info)
      return users_info
   

if __name__ == '__main__':
   device_dict = json.loads('''{
            "id": "7256eb75-f438-46dc-b364-93b97aeecd78",
            "alert_count": 0,
            "name": "Maq México 8000",
            "description": "8000 México",
            "ip": "192.168.0.101",
            "port": 502,
            "active": true,
            "is_excluded": false,
            "debug_mode": false,
            "address": "México",
            "latitude": "23.65851160",
            "longitude": "-102.00770970",
            "config_file": "http://multipetcloud.com.br/media/config/files/7256eb75-f438-46dc-b364-93b97aeecd78/05_04_2023_08_50_46/V.025.023.001_-_AB_3OGLHig.kas",
            "status": 3,
            "is_running": 0,
            "serial_number": "025.075.09-23",
            "node": {
                "id": "8f82d2fe-75d9-45e6-97ad-07362f137c1d",
                "name": "PC México",
                "ip": null,
                "icinga_id": "8f82d2fe-75d9-45e6-97ad-07362f137c1d",
                "ticket": "35164259b6272da55ced2556a4f28dd676255bf9",
                "token": "ovecloud-I9YIPM96EC",
                "local_fqdn": "PC-T4",
                "master_fqdn": "icinga2",
                "status": "DOWN",
                "last_connection": null,
                "auto_scan": false,
                "available_update_variable_maps": false,
                "update_logs": false,
                "additional_settings": {},
                "so_type": "WINDOWS",
                "company": {
                    "id": "aa158aad-bd50-43db-a585-2e912a12f7da",
                    "name": "Multipet",
                    "cnpj": "01630749000185",
                    "address": "Avenida Nossa Senhora de Fatima, 1590",
                    "phone": "(45)3056-1800",
                    "comments": null,
                    "staff": true,
                    "logo": null,
                    "dashboards": []
                }
            },
            "model": {
                "id": "146536dd-ac7e-412a-b590-a0afd8d0e639",
                "name": "Sopradora Multipet 8.000",
                "image": "http://multipetcloud.com.br/media/images/8000.JPG"
            }
        }''')
   
   device = Device(device_dict)
   device._get_company_users()
