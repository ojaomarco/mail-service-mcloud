"""Icinga API and Icinga Director functions."""

import logging
import re
import pandas as pd
from elasticsearch import Elasticsearch
import json
import datetime
from datetime import datetime
from email_service.mail_client import MailClient

class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


def dict2obj(d):
    return json.loads(json.dumps(d), object_hook=obj)


DISCOVER_DEFAULT_INDEX = "logstash*"

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
            logger.debug(
                'Getting device info from elasticsearch. Device: "%s". Node: "%s".',
                device.id,
                node.name,
            )
            query = {
                "query": {
                    "bool": {
                        "must": [{"match": {"icinga.service.keyword": f"{device.id}"}}],
                        "filter": {
                            "range": {"@timestamp": {"gte": f"now-{time_minutes}m"}}
                        },
                    }
                },
                "sort": [{"@timestamp": {"order": "desc"}}],
            }
            elastic_query_response = self.search(
                index=DISCOVER_DEFAULT_INDEX, body=query
            )

            hits = elastic_query_response.get("hits", {}).get("hits", [])

            for hit in hits:
                # takes the first result because it is the last information obtained from the system
                discover_result = hit.get("_source", {}).get("output", {})
                if discover_result:
                    return discover_result
                del hits[0]
        except Exception as error:
            logger.exception(
                'Error in ElasticCustomClient:get_device_info. Error: "%s"', error
            )
        return device_info

    def get_devices_info_new(self, devices, time_minutes):
        """Get devices info from new format of elasticsearch"""
        query = []
        results = []
        for device in devices:
            query.extend(
                [
                    {"index": DISCOVER_DEFAULT_INDEX},
                    {
                        "size": 0,
                        "aggs": {
                            "intervalos_de_tempo": {
                                "date_histogram": {
                                    "field": "@timestamp",
                                    "fixed_interval": "5m",
                                    "min_doc_count": 1,
                                },
                                "aggs": {"seus_documentos": {"top_hits": {"size": 1}}},
                            }
                        },
                        "query": {
                            "bool": {
                                "must": [
                                    {"match": {"device_id.keyword": f"{device.id}"}},
                                    {"match": {"node_id.keyword": f"{device.node.id}"}},
                                ],
                                "filter": {
                                    "range": {
                                        "@timestamp": {"gte": f"now-{time_minutes}m"}
                                    }
                                },
                            }
                        },
                        "sort": [{"@timestamp": {"order": "desc"}}],
                    },
                ]
            )
        elastic_query_response = self.msearch(body=query)

        eqr = elastic_query_response.get("responses")[0]["aggregations"][
            "intervalos_de_tempo"
        ]["buckets"]

        for doc in eqr:
            hit = doc["seus_documentos"]["hits"]["hits"]
            document = hit[0].get("_source", {})
            if document:
                start_date = doc["key_as_string"]
                end_date = hit[0].get("sort", [None])[0] if hit[0].get("sort") else None
                results.append(
                    {
                        "document": document,
                        "start_date": start_date,
                        "end_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[
                            :-3
                        ]
                        + "Z",
                    }
                )
        return results

    def get_current_device_value(self, variable, time_minutes: int = 1):
        """
        Get info of current variable values from device in ELK.
        """
        result = self.get_device_info(time_minutes=time_minutes)

        if variable in result.keys():
            return result.get(variable)
        return None

    @staticmethod
    def _formatar_tempo_em_horas(tempo):
        total_segundos = tempo.total_seconds()

        # Calcular as horas e minutos
        horas = int(total_segundos // 3600)
        minutos = int((total_segundos % 3600) // 60)
        # Formatando o tempo para mostrar apenas horas e minutos
        tempo_formatado = "{:02} Horas e {:02} Minutos".format(horas, minutos)
        return tempo_formatado
    
    def convert_date_format(self, data):
        # Converte a string de data para um objeto datetime
        dt = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Formata o objeto datetime para o formato desejado
        formatted_date = dt.strftime("%d/%m/%y")
        return formatted_date

    def get_info_values(self, device, time_minutes):
        device = dict2obj(device)
        first = False
        sum_prod_hora = []
        start_date = None
        end_date = None
        sum_hora_rodando = {"hora": [], "estado": []}
        sum_hora_aliment = {"hora": [], "came": []}
        for doc in self.get_devices_info_new([device], time_minutes=time_minutes):
            raw_result = doc["document"]
            start_date = start_date or doc["start_date"]  # Pega o primeiro start_date
            end_date = doc["end_date"]  # Atualiza o end_date com o mais recente
            result = raw_result["output"]
            if not first:
                first_prod_total = self._get_total_prod(result)
                if first_prod_total:
                    first = True
            last_prod_total = self._get_total_prod(result)
            sum_prod_hora.append(self._get_prod_hora(result))
            sum_hora_rodando["hora"].append(raw_result["@timestamp"])
            sum_hora_rodando["estado"].append(self._get_running_state(result))
            sum_hora_aliment["hora"].append(raw_result["@timestamp"])
            sum_hora_aliment["came"].append(self._get_aliment_state(result))

        try:
            while (
                (None in sum_prod_hora)
            ):
                sum_prod_hora.remove(None)

            prod_total = last_prod_total - first_prod_total
            avg_prod_hora = sum(sum_prod_hora) / len(sum_prod_hora)
            horas_rodando = self._calculate_running_time(sum_hora_rodando)
            horas_alimentando = self._calculate_alim_on_time(sum_hora_aliment)
            horas_rodando = self._formatar_tempo_em_horas(horas_rodando)
            horas_alimentando = self._formatar_tempo_em_horas(horas_alimentando)
            start_date = self.convert_date_format(start_date)
            end_date = self.convert_date_format(end_date)


            if prod_total < 0:
                prod_total = "Erro"

            producao_saude = prod_total - 1800000
            if producao_saude < 0:
                producao_saude = 0

            return {
                "horas_rodando": str(horas_rodando),
                "avg_prod_hora": avg_prod_hora,
                "prod_total": prod_total,
                "horas_alimentando": horas_alimentando,
                "producao_saude": producao_saude,
                "start_date": start_date,
                "end_date": end_date,
            }
        except Exception as e:
            # print(traceback.print_exception(e))
            print(f"Erro ao obter dados do dispositivo - ", device.name, "às", MailClient.tempo_atual())

    def _get_total_prod(self, result):
        string = "Total"
        variaveis_filtradas = [
            var for var in result.keys() if re.search(f".*{string}.*", var)
        ]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]
   
    def _get_prod_hora(self, result):
        string = "prod"
        string1 = "hora"
        variaveis_filtradas = [
            var
            for var in result.keys()
            if re.search(f".*{string1}.*", var.lower())
            and re.search(f".*{string}.*", var.lower())
        ]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _get_boot_ok(self, result):
        string = "bootOK"
        variaveis_filtradas = [
            var for var in result.keys() if re.search(f".*{string}.*", var.lower())
        ]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _calculate_running_time(self, registers):
        df = pd.DataFrame(registers)
        df["hora"] = pd.to_datetime(df["hora"])
        df = df.dropna()
        if not df.empty:
            df["tempo_entre_registros"] = df["hora"].diff()
            off_limit = pd.Timedelta(minutes=60)
            on_registers = df[df["tempo_entre_registros"] <= off_limit]
            running_time = on_registers["tempo_entre_registros"].sum()
            return running_time

    def _calculate_alim_on_time(self, registers):
        df = pd.DataFrame(registers)
        df["hora"] = pd.to_datetime(df["hora"])
        df = df.dropna()
        if not df.empty:
            df["tempo_entre_registros"] = df["hora"].diff()
            off_limit = pd.Timedelta(minutes=60)
            on_registers = df[df["tempo_entre_registros"] <= off_limit]
            running_time = on_registers["tempo_entre_registros"].sum()
            return running_time

    def _get_running_state(self, result):
        string = "boBootOK"
        string_vblow = "boBootOK"
        variaveis_filtradas = [
            var
            for var in result.keys()
            if re.search(string, var) or re.search(string_vblow, var)
        ]
        for key in result:
            if key in variaveis_filtradas:
                if result[key]:
                    return result[key]

    def _get_aliment_state(self, result):
        string = "IOs__DO_CameForno"
        string_vblow = "Auto__Alimenta"
        variaveis_filtradas = [
            var
            for var in result.keys()
            if re.search(string, var) or re.search(string_vblow, var)
        ]
        for key in result:
            if key in variaveis_filtradas:
                if result[key]:
                    return result[key]

if __name__ == "__main__":
    http_auth = ("multipet", "multipet@2022#$")
    teste = {
        "id": "ff0870c4-d127-4c5b-ac9c-e3e1ca166483",
        "alert_count": 0,
        "name": "10000 - Quinari",
        "description": None,
        "ip": "192.168.0.101",
        "port": 502,
        "active": "true",
        "is_excluded": "false",
        "debug_mode": "false",
        "address": "Ponta Grossa",
        "latitude": "0.00000000",
        "longitude": "0.00000000",
        "config_file": None,
        "status": 0,
        "is_running": 1,
        "serial_number": "",
        "node": {
            "id": "dc72b7f3-dc57-477b-a0c8-07b2dfb30236",
            "name": "Quinari",
            "ip": None,
            "icinga_id": "dc72b7f3-dc57-477b-a0c8-07b2dfb30236",
            "ticket": None,
            "token": "ovecloud-rabLFYwBXO",
            "local_fqdn": "QUINARI",
            "master_fqdn": "icinga2",
            "status": "UP",
            "last_connection": "28/06/2024 14:02:10",
            "auto_scan": "false",
            "available_update_variable_maps": "false",
            "update_logs": "false",
            "additional_settings": {"tasks": {"reader": {"frequency": 10}}},
            "so_type": "LINUX",
            "company": {
                "id": "0bc5d64c-77d3-4125-ac85-6e51c565a5e1",
                "name": "INDUSTRIA E COM. DE BEBIDAS QUINARI LTDA",
                "cnpj": "08519021000120",
                "address": None,
                "phone": None,
                "comments": "Rogleilson - 68992389686",
                "staff": "false",
                "logo": None,
                "dashboards": [
                    "3d98745b-e712-4801-84ff-a342229b4d95",
                    "ec7e5f71-09fc-4c2e-9921-30641191d29c",
                ],
            },
        },
        "model": {
            "id": "0cdcfd58-9ef8-4f7e-9779-b51a7ae621e7",
            "name": "Sopradora Multipet 10.000",
            "image": None,
        },
    }

    es = ElasticCustomCLient(["http://167.114.191.57:9200"], http_auth=http_auth)
    es.get_info_values(teste, 1440)
