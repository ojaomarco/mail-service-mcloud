"""Icinga API and Icinga Director functions."""
import logging
import re
from dateutil.parser import parse
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import json
import traceback

class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

def dict2obj(d):
    return json.loads(json.dumps(d), object_hook=obj)

DISCOVER_DEFAULT_INDEX = 'logstash*'

logger = logging.getLogger(__name__)

class ElasticCustomCLient(Elasticsearch):
    """
    Class to compile default requests in Elasticsearch and implements other functions.
    """
    def get_device_info(self, time_minutes: int = 1):
        """Get result checkout from elastic"""
        device_info = {}
        try:
            node = device.node
            logger.debug('Getting device info from elasticsearch. Device: "%s". Node: "%s".', device.id, node.name)
            query = {'query': {'bool': {'must': [{'match': {'icinga.service.keyword': f'{device.id}'}}],
                                        'filter': {'range': {'@timestamp': {'gte': f'now-{time_minutes}m'}}}}},
                    "sort": [{
                        "@timestamp": {
                            "order": "desc"
                        }
                    }]}
            elastic_query_response = self.search(index=DISCOVER_DEFAULT_INDEX, body=query)
            
            hits = elastic_query_response.get('hits', {}).get('hits', [])

            for hit in hits:
                # takes the first result because it is the last information obtained from the system
                discover_result = hit.get('_source', {}).get('output', {})
                if discover_result:
                    return discover_result
                del hits[0]
        except Exception as error:
            logger.exception('Error in ElasticCustomClient:get_device_info. Error: "%s"', error)
        return device_info

    def get_devices_info_new(self, devices, time_minutes):
        """Get devices info from new format of elasticsearch"""
        query = []
        results = []
        for device in devices:
            query.extend([  {'index': DISCOVER_DEFAULT_INDEX},
                            {'size': 0, 
                            'aggs': {
                                    'intervalos_de_tempo': {
                                        'date_histogram': {
                                            'field': '@timestamp',
                                            'fixed_interval': '1800000ms',
                                            'min_doc_count': 1
                                        },
                                        'aggs': {
                                            'seus_documentos': {
                                                'top_hits': {
                                                    'size': 1  
                                                }
                                            }
                                        }
                                    }
                                }, 
                                'query': {'bool': {'must': [
                                    {'match': {'device_id.keyword': f'{device.id}'}},
                                    {'match': {'node_id.keyword': f'{device.node.id}'}}],
                                'filter': {'range': {'@timestamp': {'gte': f'now-{time_minutes}m'}}}}},
                                "sort": [{
                                    "@timestamp": {
                                        "order": "desc"
                                    }
                        }]}])
        elastic_query_response = self.msearch(body=query)

        eqr = elastic_query_response.get('responses')[0]['aggregations']['intervalos_de_tempo']['buckets']

        for doc in eqr:
            hit = doc['seus_documentos']['hits']['hits']
            document = hit[0].get('_source', {})
            if document:
                results.append(document)
        return results

    def get_current_device_value(self, variable, time_minutes: int = 1):
        """
        Get info of current variable values from device in ELK.
        """
        result = self.get_device_info( time_minutes=time_minutes)
        if variable in result.keys():
            return result.get(variable)
        return None
    
    def get_alerts_values(self, time_minutes):
        alerts = []
        for doc in self.get_devices_info_new([device], time_minutes=time_minutes):
            raw_result = doc
            result = raw_result["output"]
            # print(result)
            string = "Total"
            variaveis_filtradas = [var for var in result.keys() if re.search(f".*{string}.*", var)]
            
            final_dict = {}
            for key in result:
                
                if key in variaveis_filtradas:
                    print(result[key])
                    if result[key] == 1:
                        final_dict[raw_result['@timestamp']] = key
            alerts.append(final_dict)
        self.group_alerts(alerts)

    def get_info_values(self, device, time_minutes):
        device = dict2obj(device)
        first = False
        sum_press_baixa = []
        sum_press_alta = []
        sum_temp_coifa = []
        sum_prod_hora = []
        sum_hora_rodando = []
        for doc in self.get_devices_info_new([device], time_minutes=time_minutes):
            raw_result = doc
            result = raw_result["output"]
            if not first:
                first_prod_total = self._get_total_prod(result)
                first = True 
            sum_temp_coifa.append(self._get_temp_coifa(result))
            last_prod_total = self._get_total_prod(result)
            sum_prod_hora.append(self._get_prod_hora(result))
            sum_press_baixa.append(self._get_press_baixa(result))
            sum_press_alta.append(self._get_press_alta(result))
            sum_hora_rodando.append({'Run': raw_result["@timestamp"]})
        
        try:
            horas_rodando = self._calculate_running_time(sum_hora_rodando)
            avg_temp_coifa = sum(sum_temp_coifa) / len(sum_temp_coifa)
            avg_press_baixa = sum(sum_press_baixa) / len(sum_press_baixa)
            avg_press_alta = sum(sum_press_alta) / len(sum_press_alta)
            prod_total = last_prod_total - first_prod_total
            avg_prod_hora = sum(sum_prod_hora) / len(sum_prod_hora)
            print(device.name ,last_prod_total, first_prod_total, prod_total)

            return ({'horas_rodando':str(horas_rodando), 'avg_prod_hora': avg_prod_hora, 'avg_press_alta':avg_press_alta, 'avg_press_baixa':avg_press_baixa, 'prod_total':prod_total, 'avg_temp_coifa':avg_temp_coifa})
        except:
            print('erro ao obter dados do dispositivo')
  
    def _get_total_prod(self, result):
        string = "Total"
        variaveis_filtradas = [var for var in result.keys() if re.search(f".*{string}.*", var)]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _get_press_baixa(self, result):
        string = "Baixa"
        string1 = "Analog"
        variaveis_filtradas = [var for var in result.keys() if re.search(f".*{string1}.*", var) and re.search(f".*{string}.*", var)]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _get_press_alta(self, result):
        string = "Alta"
        string1 = "Analog"
        variaveis_filtradas = [var for var in result.keys() if re.search(f".*{string1}.*", var) and re.search(f".*{string}.*", var)]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]
            
    def _get_temp_coifa(self, result):
        string = "Coifa"
        string1 = "Analog"
        variaveis_filtradas = [var for var in result.keys() if re.search(f".*{string1}.*", var) and re.search(f".*{string}.*", var)]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]    
                
    def _get_prod_hora(self, result):
        string = "prod"
        string1 = "hora"
        variaveis_filtradas = [var for var in result.keys() if re.search(f".*{string1}.*", var.lower()) and re.search(f".*{string}.*", var.lower())]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _get_boot_ok(self, result):
        string = "boot"
        variaveis_filtradas = [var for var in result.keys() if re.search(f".*{string}.*", var.lower())]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]   

    def _calculate_running_time(self, registers):
        df = pd.DataFrame(registers)
        df['Run'] = pd.to_datetime(df['Run'])
       
        if not df.empty:
            df['tempo_entre_registros'] = df['Run'].diff()
            off_limit = pd.Timedelta(minutes=60)
            on_registers = df[df['tempo_entre_registros'] <= off_limit]
            running_time = on_registers['tempo_entre_registros'].sum()
            return running_time

if __name__ == '__main__':
    http_auth = ('multipet', 'multipet@2022#$')
    teste = {
    "id": "5579bf4d-beee-4c18-ab15-996faa8743db",
    "alert_count": 0,
    "name": "10000 LINUX DELRIO",
    "description": None,
    "ip": "192.168.0.111",
    "port": 502,
    "active": True,
    "is_excluded": False,
    "debug_mode": False,
    "address": "DELRIO",
    "latitude": "34.47280890",
    "longitude": "-93.18015960",
    "config_file": None,
    "status": 0,
    "is_running": 1,
    "serial_number": "",
    "node": {
        "id": "6eed7bd4-6505-4576-9b9a-3457bce4a151",
        "name": "DelRio Linux",
        "ip": None,
        "icinga_id": "6eed7bd4-6505-4576-9b9a-3457bce4a151",
        "ticket": None,
        "token": "ovecloud-zy0Aim50YV",
        "local_fqdn": "PC-LINUX",
        "master_fqdn": "icinga2",
        "status": "UP",
        "last_connection": "22/02/2024 14:33:29",
        "auto_scan": False,
        "available_update_variable_maps": False,
        "update_logs": False,
        "additional_settings": {
            "tasks": {
                "reader": {
                    "frequency": 10
                }
            }
        },
        "so_type": "LINUX",
        "company": {
            "id": "2ccc6d34-faa6-47f7-bc92-cfdbcdf3103c",
            "name": "DelRio Refrigerantes",
            "cnpj": "07815053000100",
            "address": None,
            "phone": None,
            "comments": None,
            "staff": False,
            "logo": None,
            "dashboards": [
                "3d98745b-e712-4801-84ff-a342229b4d95",
                "a7f5da8f-79c2-494b-a35d-98e6945f956a",
                "ec7e5f71-09fc-4c2e-9921-30641191d29c"
            ]
        }
    },
    "model": {
        "id": "0cdcfd58-9ef8-4f7e-9779-b51a7ae621e7",
        "name": "Sopradora Multipet 10.000",
        "image": None
    }
    }
    es = ElasticCustomCLient(['http://167.114.191.57:9200'], http_auth=http_auth)
    print(es.get_info_values(teste, 1440))
   
