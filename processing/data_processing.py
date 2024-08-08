import pandas as pd
from pandas.tseries.offsets import DateOffset
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
        self.all_issues = client.get_all_issues()
        self.all_faults = client.get_all_faults()

    def process_data(self):
        processed_data = {}
        for device in self.devices:
            obj_device = Device(device)
            info_data = self.es_client.get_info_values(device, 1440)
            processed_data[obj_device.id_device] = {
                "users": obj_device._get_company_users(self.all_users),
                "description": obj_device.description,
                "status": obj_device.status,
                "is_running": obj_device.is_running,
                "serial_number": obj_device.serial_number,
                "info_data": info_data,
                "issues": (
                    self.process_issues(self.all_issues.get(obj_device.id_device, []))
                    if info_data
                    else None
                ),
                "fault_time": (
                    self.get_duracao(self.all_faults.get(obj_device.id_device, []))
                    if info_data
                    else None
                ),
            }
            (
                logging.info(f"{[obj_device.id_device]} Device has all data.")
                if info_data
                else logging.info(
                    f"{[obj_device.id_device]} Device has not all data. Device offline. {obj_device.is_running}"
                )
            )

        return processed_data

    def process_issues(self, issues):
        try:
            df = pd.DataFrame(issues)
            df["name"] = df["name"].map(alert).fillna(df["name"])
            df["name"] = df["name"].map(fault).fillna(df["name"])
            df["opened_at"] = pd.to_datetime(df["opened_at"])
            df["closed_at"] = pd.to_datetime(df["closed_at"])
            df = df[["opened_at", "closed_at", "name"]]

            df = df.sort_values(by=["name", "opened_at", "closed_at"], ascending=True)
            df["diff"] = df["opened_at"].diff()
            df.reset_index(drop=True, inplace=True)
            rows_to_remove = []
            for i in range(1, len(df)):
                if df.iloc[i]["name"] == df.iloc[i - 1]["name"]:
                    if df.iloc[i]["diff"] < pd.Timedelta(minutes=15):
                        rows_to_remove.append(i)

            result = df.drop(rows_to_remove)
            result.reset_index(drop=True, inplace=True)
            result = result.sort_values(by=["opened_at"], ascending=True)
            """Correção da tabela de falhas, agora mostra o horário certo -3h"""
            result["opened_at"] = pd.to_datetime(result["opened_at"]) - DateOffset(
                hours=3
            )
            result["closed_at"] = pd.to_datetime(result["closed_at"]) - DateOffset(
                hours=3
            )

            result["opened_at_str"] = result["opened_at"].dt.strftime("%d/%m %H:%M")
            result["closed_at_str"] = result["closed_at"].dt.strftime("%d/%m %H:%M")

            result["closed_at_str"] = result["closed_at_str"].fillna(
                ""
            )  # Substituir NaN por vazio

            result["duracao"] = result["closed_at"] - result["opened_at"]

            result = result[["opened_at_str", "closed_at_str", "name"]]
            result.columns = ["Hora Início", "Hora Fim", "Descrição"]

            html_table = result.to_html(index=False, classes="table", border=False)

            # Apply the highlighting function to each cell in the "Descrição" column
            for i in range(len(result)):
                if result.iloc[i]["Descrição"] in fault.values():
                    html_table = html_table.replace(
                        f'<td>{result.iloc[i]["Descrição"]}</td>',
                        f'<td style="font-weight: bold;">{result.iloc[i]["Descrição"]}</td>',
                    )

            return html_table

        except Exception as e:
            logging.error(f"Error: process issues failed. Error details: {str(e)}")
            return

    def get_duracao(self, faults):

        try:
            df = pd.DataFrame(faults)
            df["name"] = df["name"].map(alert).fillna(df["name"])
            df["name"] = df["name"].map(fault).fillna(df["name"])
            df["opened_at"] = pd.to_datetime(df["opened_at"])
            df["closed_at"] = pd.to_datetime(df["closed_at"])
            df = df[["opened_at", "closed_at", "name"]]

            df = df.sort_values(by=["opened_at", "closed_at"], ascending=True)

            # Mesclar intervalos de falhas sobrepostos
            merged_intervals = []
            current_start = df.iloc[0]["opened_at"]
            current_end = df.iloc[0]["closed_at"]

            for i in range(1, len(df)):
                row = df.iloc[i]
                if row["opened_at"] <= current_end:
                    current_end = max(current_end, row["closed_at"])
                else:
                    merged_intervals.append((current_start, current_end))
                    current_start = row["opened_at"]
                    current_end = row["closed_at"]

            merged_intervals.append((current_start, current_end))

            # Criar DataFrame a partir dos intervalos mesclados
            merged_df = pd.DataFrame(
                merged_intervals, columns=["opened_at", "closed_at"]
            )

            merged_df["opened_at_str"] = merged_df["opened_at"].dt.strftime(
                "%d/%m %H:%M"
            )
            merged_df["closed_at_str"] = merged_df["closed_at"].dt.strftime(
                "%d/%m %H:%M"
            )

            merged_df["duracao"] = merged_df["closed_at"] - merged_df["opened_at"]

            merged_df = merged_df[["opened_at_str", "closed_at_str", "duracao"]]
            merged_df.columns = ["Hora Início", "Hora Fim", "Duração"]

            self.result = merged_df
            self.duracao_total = merged_df["Duração"].sum()

            tempo = ElasticCustomCLient._formatar_tempo_em_horas(self.duracao_total)

            return tempo

        except Exception as e:
            logging.error(f"Error: process issues failed. Error details: {str(e)}")
            return
