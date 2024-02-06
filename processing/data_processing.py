import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from api_consumer.api_client import Client
from processing.models.device import Device



class Processer():
    def __init__(self, client: Client):
        self.client = client
        self.devices = client.get_all_devices()
        self.all_users =  client.get_all_users()
        
    def process_data(self):
        processed_data = {}
        for device in self.devices:
            device = Device(device)
            processed_data[device.id_device] = {'users': device._get_company_users(self.all_users), 
                                                'description': device.description, 
                                                'status' : device.status,
                                                'is_running' : device.is_running,
                                                'serial_number' : device.serial_number 
                                                }
        return(processed_data)
    

if __name__ == '__main__':
    client =  Client()
    processer = Processer(client)
    print(processer.process_data())

