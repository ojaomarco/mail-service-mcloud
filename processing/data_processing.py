import logging
from config.base import alert, fault
from api_consumer.api_client import Client
from processing.models.device import Device
from api_consumer.es_client import ElasticCustomCLient


class Processer:
    def __init__(self, client: Client, es_client: ElasticCustomCLient):
        self.es_client = es_client
        self.client = client
        self.devices = client.get_all_devices()
        self.all_users = client.get_all_users()

    def process_data(self):
        processed_data = {}
        for device in self.devices:
            obj_device = Device(device)
            info_data = self.es_client.get_info_values(device, 43920)
            processed_data[obj_device.id_device] = {
                "users": obj_device._get_company_users(self.all_users),
                "description": obj_device.description,
                "status": obj_device.status,
                # "is_running": obj_device.is_running,
                "serial_number": obj_device.serial_number,
                "info_data": info_data,
            }
            (
                logging.info(f"{[obj_device.id_device]} Device has all data.")
                if info_data
                else logging.info(
                    f"{[obj_device.id_device]} Device has not all data. Device offline. {obj_device.is_running}"
                )
            )

        return processed_data
