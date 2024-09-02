"""Icinga API and Icinga Director functions."""

import logging
import re
from dateutil.parser import parse
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import json
import traceback
import datetime


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
                                    "fixed_interval": "1800000ms",
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
                results.append(document)
        return results

    def get_current_device_value(self, variable, time_minutes: int = 1):
        """
        Get info of current variable values from device in ELK.
        """
        result = self.get_device_info(time_minutes=time_minutes)

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
            variaveis_filtradas = [
                var for var in result.keys() if re.search(f".*{string}.*", var)
            ]

            final_dict = {}
            for key in result:

                if key in variaveis_filtradas:
                    if result[key] == 1:
                        final_dict[raw_result["@timestamp"]] = key
            alerts.append(final_dict)
        self.group_alerts(alerts)

    @staticmethod
    def _formatar_tempo_em_horas(tempo):
        total_segundos = tempo.total_seconds()

        # Calcular as horas e minutos
        horas = int(total_segundos // 3600)
        minutos = int((total_segundos % 3600) // 60)
        # Formatando o tempo para mostrar apenas horas e minutos
        tempo_formatado = "{:02} Horas e {:02} Minutos".format(horas, minutos)
        return tempo_formatado

    def get_info_values(self, device, time_minutes):
        device = dict2obj(device)
        first = False
        sum_press_baixa = []
        sum_press_alta = []
        sum_temp_coifa = []
        sum_prod_hora = []
        sum_hora_rodando = []
        sum_hora_aliment = {"hora": [], "came": []}
        for doc in self.get_devices_info_new([device], time_minutes=time_minutes):
            raw_result = doc
            result = raw_result["output"]
            if not first:
                first_prod_total = self._get_total_prod(result)
                if first_prod_total:
                    first = True
            sum_temp_coifa.append(self._get_temp_coifa(result))
            last_prod_total = self._get_total_prod(result)
            sum_prod_hora.append(self._get_prod_hora(result))
            sum_press_baixa.append(self._get_press_baixa(result))
            sum_press_alta.append(self._get_press_alta(result))
            sum_hora_rodando.append({"Run": raw_result["@timestamp"]})
            sum_hora_aliment["hora"].append(raw_result["@timestamp"])
            sum_hora_aliment["came"].append(self._get_aliment_state(result))

        try:
            while (
                (None in sum_temp_coifa)
                or (None in sum_press_baixa)
                or (None in sum_press_alta)
                or (None in sum_prod_hora)
            ):
                sum_temp_coifa.remove(None)
                sum_press_alta.remove(None)
                sum_press_baixa.remove(None)
                sum_prod_hora.remove(None)

            horas_rodando = self._calculate_running_time(sum_hora_rodando)

            avg_temp_coifa = sum(sum_temp_coifa) / len(sum_temp_coifa)
            avg_press_baixa = sum(sum_press_baixa) / len(sum_press_baixa)
            avg_press_alta = sum(sum_press_alta) / len(sum_press_alta)

            prod_total = last_prod_total - first_prod_total
            avg_prod_hora = sum(sum_prod_hora) / len(sum_prod_hora)
            horas_alimentando = self._calculate_alim_on_time(sum_hora_aliment)
            eficiencia = self._calculate_efficiency(
                avg_prod_hora, horas_rodando, prod_total
            )
            horas_rodando = self._formatar_tempo_em_horas(horas_rodando)
            horas_alimentando = self._formatar_tempo_em_horas(horas_alimentando)
            grafico_eficiencia = self.generate_graphic_efficiency(eficiencia)
            informacoes_grafico = self.generate_graphic(
                sum_press_baixa, sum_hora_aliment["hora"], sum_press_alta
            )
            """
            print(
                device.name,
                last_prod_total,
                first_prod_total,
                prod_total,
                horas_rodando,
                horas_alimentando,
            )
            """
            return {
                "horas_rodando": str(horas_rodando),
                "avg_prod_hora": avg_prod_hora,
                "avg_press_alta": avg_press_alta,
                "avg_press_baixa": avg_press_baixa,
                "prod_total": prod_total,
                "avg_temp_coifa": avg_temp_coifa,
                "horas_alimentando": horas_alimentando,
                "informacoes_grafico": informacoes_grafico,
                "eficiencia": eficiencia,
                "grafico_eficiencia": grafico_eficiencia,
            }
        except Exception as e:
            # print(traceback.print_exception(e))
            print(f"Erro ao obter dados do dispositivo ", device.name)

    def _get_total_prod(self, result):
        string = "Total"
        variaveis_filtradas = [
            var for var in result.keys() if re.search(f".*{string}.*", var)
        ]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _get_press_baixa(self, result):
        string = "Baixa"
        string1 = "Analog"
        variaveis_filtradas = [
            var
            for var in result.keys()
            if re.search(f".*{string1}.*", var) and re.search(f".*{string}.*", var)
        ]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _get_press_alta(self, result):
        string = "Alta"
        string1 = "Analog"
        variaveis_filtradas = [
            var
            for var in result.keys()
            if re.search(f".*{string1}.*", var) and re.search(f".*{string}.*", var)
        ]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _get_temp_coifa(self, result):
        string = "Coifa"
        string1 = "Analog"
        variaveis_filtradas = [
            var
            for var in result.keys()
            if re.search(f".*{string1}.*", var) and re.search(f".*{string}.*", var)
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
        string = "boot"
        variaveis_filtradas = [
            var for var in result.keys() if re.search(f".*{string}.*", var.lower())
        ]
        for key in result:
            if key in variaveis_filtradas:
                return result[key]

    def _calculate_running_time(self, registers):
        df = pd.DataFrame(registers)
        df["Run"] = pd.to_datetime(df["Run"])
        if not df.empty:
            df["tempo_entre_registros"] = df["Run"].diff()
            off_limit = pd.Timedelta(minutes=60)
            on_registers = df[df["tempo_entre_registros"] <= off_limit]
            running_time = on_registers["tempo_entre_registros"].sum()
            return running_time

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

    @staticmethod
    def _calculate_efficiency(vel_media, time, total):
        total_segundos = time.total_seconds()

        # Calcular as horas e minutos
        horas = int(total_segundos // 3600)
        minutos = int((total_segundos % 3600) // 60)

        # Convertendo o tempo total para horas (adicionando as horas às horas fracionadas pelos minutos)
        tempo_total_horas = horas + (minutos / 60)
        # Calculando a eficiência
        producao = vel_media * tempo_total_horas
        eficiencia = (total * 100) / producao

        if eficiencia > 100:
            eficiencia = 100

        return round(eficiencia)

        # return eficiencia

    def generate_graphic(self, data_low, time, data_high):
        hours = []
        data_high = [round(x, 2) for x in data_high]
        data_low = [round(x, 2) for x in data_low]

        for timestamp in time:
            dt_obj = datetime.datetime.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
            hours_minute = dt_obj.strftime("%H:%M")
            hours.append(hours_minute)
        base = {
            "type": "line",
            "data": {
                "labels": hours,
                "datasets": [
                    {
                        "label": "Pressão baixa",
                        "data": data_low,
                        "fill": "false",
                        "backgroundColor": "rgb(255, 99, 132)",
                        "borderColor": "rgb(255, 99, 132)",
                    },
                    {
                        "label": "Pressão alta",
                        "data": data_high,
                        "fill": "false",
                        "backgroundColor": "rgb(54, 162, 235)",
                        "borderColor": "rgb(54, 162, 235)",
                    },
                ],
            },
        }

        url = f"https://quickchart.io/chart?v=2.9.4&c={base}"
        return url

    def generate_graphic_efficiency(self, data):
        base = {
            "type": "radialGauge",
            "data": {"datasets": [{"data": [data], "backgroundColor": "blue"}]},
            "options": {
                "responsive": "true",
                "legend": {},
                "title": {"display": "true", "text": ""},
                "centerPercentage": 90,
                "centerArea": {
                    "text": f"{data}%",
                    "subText": "Eficiência",
                },
            },
        }

        url = f"https://quickchart.io/chart?v=2.9.4&c={base}"
        return url


if __name__ == "__main__":
    http_auth = ("multipet", "multipet@2022#$")
    teste = {
        "id": "6d0e9a55-a703-4e87-a27f-86433291320d",
        "alert_count": 0,
        "name": "VBlow Santa Rita",
        "description": None,
        "ip": "192.168.0.101",
        "port": 502,
        "active": "true",
        "is_excluded": "false",
        "debug_mode": "false",
        "address": "Rancho Queimado",
        "latitude": "0.00000000",
        "longitude": "0.00000000",
        "config_file": None,
        "status": 0,
        "is_running": 1,
        "serial_number": "044.002.36-23",
        "node": {
            "id": "513f5a3f-5d6c-4800-83d0-86309f463fc1",
            "name": "Santa Rita",
            "ip": "null",
            "icinga_id": "513f5a3f-5d6c-4800-83d0-86309f463fc1",
            "ticket": "null",
            "token": "ovecloud-Ki9FOZYykW",
            "local_fqdn": "SANTARITA",
            "master_fqdn": "icinga2",
            "status": "UP",
            "last_connection": "16/05/2024 11:33:15",
            "auto_scan": "false",
            "available_update_variable_maps": "false",
            "update_logs": "false",
            "additional_settings": {"tasks": {"reader": {"frequency": 10}}},
            "so_type": "LINUX",
            "company": {
                "id": "2154ef78-bf8e-450a-8199-e213c2ee2189",
                "name": "ESTANCIA HIDROM. STA RITA DE CASSIA LTDA",
                "cnpj": "03489027000188",
                "address": None,
                "phone": None,
                "comments": "João - 48 9949-8856",
                "staff": "false",
                "logo": None,
                "dashboards": [],
            },
        },
        "model": {
            "id": "60162c80-1a1b-4363-b219-22f705fae52e",
            "name": "V-BLOW",
            "image": None,
        },
    }
    es = ElasticCustomCLient(["http://167.114.191.57:9200"], http_auth=http_auth)
    es.get_info_values(teste, 1440)
