import sys
import os
import pandas as pd
import logging
from config.base import alert, fault
from api_consumer.api_client import Client
from processing.models.device import Device
from api_consumer.es_client import ElasticCustomCLient

class Processer():
    def __init__(self, client: Client, es_client: ElasticCustomCLient):
        self.es_client = es_client
        self.client = client
        self.devices = client.get_all_devices()
        self.all_users =  client.get_all_users()
        self.all_issues = client.get_all_issues()
        
    def process_data(self):
        processed_data = {}
        for device in self.devices:
            obj_device = Device(device)
            info_data =  self.es_client.get_info_values(device,1440)
            processed_data[obj_device.id_device] = {'users': obj_device._get_company_users(self.all_users), 
                                                'description': obj_device.description, 
                                                'status' : obj_device.status,
                                                'is_running' : obj_device.is_running,
                                                'serial_number' : obj_device.serial_number,
                                                'info_data' : info_data,
                                                'issues' : self.process_issues(self.all_issues.get(obj_device.id_device, [])) if info_data else None
                                                }
            logging.info(f'{[obj_device.id_device]} Device has all data.') if info_data else logging.info(f'{[obj_device.id_device]} Device has not all data. Device offline. {obj_device.is_running}')

        return(processed_data)
    
    def process_issues(self, issues):
        try:
            df = pd.DataFrame(issues)
            df['name'] = df['name'].map(alert).fillna(df['name'])
            df['name'] = df['name'].map(fault).fillna(df['name'])
            df["opened_at"] = pd.to_datetime(df["opened_at"])
            df = df[["opened_at", "name"]]

            df = df.sort_values(by=['name','opened_at'], ascending=True)
            df['diff'] = df['opened_at'].diff()
            df.reset_index(drop=True, inplace=True)
            rows_to_remove = []

            for i in range(1, len(df)):
                if df.iloc[i]['name'] == df.iloc[i - 1]['name']:
                    if df.iloc[i]['diff'] < pd.Timedelta(minutes=15):
                        rows_to_remove.append(i)

            result = df.drop(rows_to_remove)
            result.reset_index(drop=True, inplace=True)
            result = result.sort_values(by=['opened_at'], ascending=True)
            result["opened_at"] = pd.to_datetime(result["opened_at"]).dt.strftime('%d/%m %H:%M')
            result = result[["opened_at", "name"]]
            result.columns = ["Hora",  "Nome"]
            return result 
        except:
            logging.error('Error: process issues failed. Device offline.')


