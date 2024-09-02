import logging
import argparse
from processing.data_processing import Processer
from email_service.mail_client import MailClient
from templates.base_templates import HTML_TEMPLATE_FINANCEIRO


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
                            # data["is_running"],
                            data["info_data"],
                        )
                        logging.info(
                            f"[{k}] Dados para envio do email obtidos com sucesso."
                        )
                        MailClient.send_email(
                            html,
                            ["automacaomultipet01@gmail.com"],
                        )

        return devices_info

    @staticmethod
    def _email_builder_active(
        user,
        serial_number,
        status,
        info_data,
    ):

        try:
            html_email = HTML_TEMPLATE_FINANCEIRO.format(
                user_name=user,
                status=status,
                serial_number=serial_number,
                total_prod=round(info_data["prod_total"]),
                running_time=info_data["horas_rodando"],
                prod_hora=round(info_data["avg_prod_hora"]),
                horas_alimentando=info_data["horas_alimentando"],
                producao_saude=info_data["producao_saude"],
                start_date=info_data["start_date"],
                end_date=info_data["end_date"],
            )
            return html_email
        except:
            logging.error(f"Erro ao contruir o email do device {serial_number}")
