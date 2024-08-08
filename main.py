from rocketry import Rocketry
from rocketry.conds import daily
from email_service.sender import Sender
from config.auth import ELASTIC_AUTH
from processing.data_processing import Processer
from api_consumer.api_client import Client
from api_consumer.es_client import ElasticCustomCLient
import sys
import os
import logging
from rocketry.conds import daily

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


app = Rocketry()


@app.task(daily.between("08:30", "09:00"))
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=f"{current_dir}/logs/mail_service.log",
    )
    client = Client()
    es_client = ElasticCustomCLient(
        ["http://167.114.191.57:9200"], http_auth=ELASTIC_AUTH
    )
    processer = Processer(client, es_client)
    Sender.send_status(processer=processer)


if __name__ == "__main__":
    main()
    # Serviço principal
