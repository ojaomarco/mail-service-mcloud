from collections import defaultdict
from pandas import DateOffset
import requests
import logging
import pandas as pd
from datetime import datetime, timedelta
from config.auth import BASE_URL, AUTH, BASE_URL_ISSUE


class Client:
    def __init__(self):
        self.url = f"{BASE_URL}"

    """def get_all_devices(self):
        logging.info("[api_client] Requesting all devices.")
        data_list = []
        response = requests.get(self.url, auth=AUTH)
        data = response.json()
        for x in response.json()["results"]:
            data_list.append(x)
        while data["next"] is not None:
            response = requests.get(data["next"], auth=AUTH)
            data = response.json()
            for x in response.json()["results"]:
                data_list.append(x)

        logging.info("[api_client] All devices requested successfully.")
        return data_list"""

    def get_all_devices(self):
        logging.info("[api_client] Requesting all devices.")
        target_device_id = "373e898a-48ff-4551-8826-c9fe8a55eaac"
        data_list = []
        response = requests.get(self.url, auth=AUTH)
        data = response.json()
        for x in data["results"]:
            if x["id"] == target_device_id:
                # return x
                data_list.append(x)
        while data["next"] is not None:
            response = requests.get(data["next"], auth=AUTH)
            data = response.json()
            for x in data["results"]:
                if x["id"] == target_device_id:
                    # return x
                    data_list.append(x)

        logging.info("[api_client] All devices requested successfully.")
        return data_list

    def get_all_users(self):
        logging.info("[api_client] Requesting all users.")
        data_list = []
        response = requests.get("http://multipetcloud.com.br/api/users", auth=AUTH)
        data = response.json()
        data_list.append(response.json()["results"])
        while data["next"] is not None:
            response = requests.get(data["next"], auth=AUTH)
            data = response.json()
            data_list.append(data["results"])
        logging.info("[api_client] All users requested successfully.")
        return data_list

    def get_all_issues(self):
        logging.info("[api_client] Requesting all issues.")
        final_time = datetime.now().isoformat()
        initial_time = (datetime.now() - timedelta(hours=24)).isoformat()
        response = requests.get(
            f"{BASE_URL_ISSUE}?time_from={initial_time}Z&time_to={final_time}Z&limit=-1",
            auth=AUTH,
        )
        data = response.json()
        issues_by_device = defaultdict(list)
        for issue in data:
            issues_by_device[issue["device"]].append(issue)
        logging.info("[api_client] All issues requested successfully.")
        return issues_by_device

    def get_all_faults(self):
        logging.info("[api_client] Requesting all issues.")
        final_time = datetime.now().isoformat()
        initial_time = (datetime.now() - timedelta(hours=24)).isoformat()
        response = requests.get(
            f"{BASE_URL_ISSUE}?time_from={initial_time}Z&time_to={final_time}Z&limit=-1",
            auth=AUTH,
        )
        data = response.json()
        issues_by_device = defaultdict(list)

        for issue in data:  # Acessar a lista de resultados
            if "Fault" in issue.get(
                "category", ""
            ):  # Verificar se 'Falha' está no campo 'name'
                issues_by_device[issue["device"]].append(issue)
                logging.debug(f"Added issue: {issue}")

        logging.info("[api_client] All issues requested successfully.")
        return issues_by_device
