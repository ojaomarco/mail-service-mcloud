import logging

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
      users_info = []
      for users in data_list:
         for user in users:
            if user.get("company", {}).get("id") == self.id_company:
                user_info = {"id": user["id"], "name": f'{user["first_name"]} {user["last_name"]}' ,"email": user["email"]}
                users_info.append(user_info)
      return users_info
   