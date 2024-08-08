import logging
import argparse
from processing.data_processing import Processer
from email_service.mail_client import MailClient
from templates.base_templates import HTML_TEMPLATE
from templates.base_templates import HTML_TEMPLATE_ERRO
from config.base import fault


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
                    if user["email"]:
                        html = Sender._email_builder_active(
                            user["name"],
                            data["serial_number"],
                            data["status"],
                            data["is_running"],
                            data["info_data"],
                            data["issues"],
                            data["fault_time"],
                        )
                        logging.info(
                            f"[{k}] Dados para envio do email obtidos com sucesso."
                        )
                        MailClient.send_email(
                            html,
                            # Comentar aqui para não enviar E-mail ao cliente
                            [user["email"], "automacaomultipet01@gmail.com"],
                            data["info_data"]["informacoes_grafico"],
                            data["info_data"]["grafico_eficiencia"],
                            data["info_data"]["grafico_tempoligado"],
                            data["info_data"]["grafico_temperatura"],
                        )

                else:
                    # Enviar e-mail informando que o sistema está offline
                    if user["email"]:

                        html = Sender._email_builder_deactivated(
                            user["name"],
                            data["serial_number"],
                            data["status"],
                            data["is_running"],
                        )
                        # Comentar aqui para não enviar E-mail ao cliente
                        MailClient.send_email(html, [user["email"], "automacaomultipet01@gmail.com"])
                        logging.warning(
                            f"[{k}] Dados para envio do email não foram obtidos com sucesso"
                        )

        return devices_info

    @staticmethod
    def _email_builder_active(
        user, serial_number, status, running, info_data, issues, fault_time
    ):
        if fault_time != None:
            if fault_time > info_data["horas_rodando"]:
                fault_time = info_data["horas_rodando"]

        else:
            fault_time=0

        try:
            html_table = issues
            # html_table = issues.to_html(index=False, classes="table", border=False)

            # print(f"Type of issues: {type(html_table)}")
            # print(f"First few rows of issues:\n{issues.head()}")

            """html_table = html_table.replace(
                    "<td>", '<td style="background-color: yellow;">'
                )"""

            html_email = HTML_TEMPLATE.format(
                user_name=user,
                status=status,
                serial_number=serial_number,
                total_prod=round(info_data["prod_total"]),
                running_time=info_data["horas_rodando"],
                prod_hora=round(info_data["avg_prod_hora"]),
                press_baixa=round(info_data["avg_press_baixa"], 1),
                press_alta=round(info_data["avg_press_alta"], 1),
                horas_alimentando=info_data["horas_alimentando"],
                # temp_coifa=round(info_data["avg_temp_coifa"], 1),
                issues_table=html_table,
                fault_time=fault_time,
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
