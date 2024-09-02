import logging
import sys
import os
import argparse
import time
import pandas as pd
from processing.data_processing import Processer
from elasticsearch import Elasticsearch
from email_service.mail_client import MailClient
from templates.base_templates import HTML_TEMPLATE
from templates.base_templates import HTML_TEMPLATE_ERRO


class Sender:
    """
    Class to send the emails with the correct information
    """

    def __init__(
        self,
    ):

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="send emails to mcloud users",
        )
        parser.add_argument("")

    @staticmethod
    def send_status(processer: Processer):
        devices_info = processer.process_data()
        for k, data in devices_info.items():
            for user in data["users"]:
                if data["info_data"]:
                    # print(data["info_data"])
                    # enviar email com status das ultimas 24 horas
                    if user["email"]:
                        html = Sender._email_builder_active(
                            user["name"],
                            data["serial_number"],
                            data["status"],
                            data["is_running"],
                            data["info_data"],
                            data["issues"],
                        )
                        logging.info(
                            f"[{k}] Dados para envio do email obtidos com sucesso."
                        )
                        MailClient.send_email(
                            html,
                            ["automacaomultipet01@gmail.com"],
                            data["info_data"]["informacoes_grafico"],
                            data["info_data"]["grafico_eficiencia"],
                        )

                else:
                    # enviar email informando que o sistema ta off solicitando contato
                    if user["email"]:

                        html = Sender._email_builder_deactivated(
                            user["name"],
                            data["serial_number"],
                            data["status"],
                            data["is_running"],
                        )
                        # MailClient.send_email(html, [user["email"]])
                        logging.warning(
                            f"[{k}] Dados para envio do email não foram obtidos com sucesso"
                        )

        return devices_info

    @staticmethod
    def _email_builder_active(
        user, serial_number, status, is_running, info_data, issues
    ):
        try:
            html_table = issues.to_html(index=False, classes="table", border=False)
            html_email = HTML_TEMPLATE.format(
                user_name=user,
                status=status,
                serial_number=serial_number,
                total_prod=round(info_data["prod_total"]),
                running_time=info_data["horas_rodando"],
                prod_hora=round(info_data["avg_prod_hora"]),
                press_baixa=round(info_data["avg_press_baixa"], 1),
                press_alta=round(info_data["avg_press_alta"], 1),
                temp_coifa=round(info_data["avg_temp_coifa"], 1),
                issues_table=html_table,
                horas_alimentando=info_data["horas_alimentando"],
            )
            return html_email
        except:
            logging.error(f"Erro ao contruir o email do device {serial_number}")

    @staticmethod
    def _email_builder_deactivated(user, serial_number, status, is_running):
        html_email = HTML_TEMPLATE_ERRO.format(
            user_name=user,
            status=status,
            serial_number=serial_number,
            is_running=is_running,
        )

        return html_email
