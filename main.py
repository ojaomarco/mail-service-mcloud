import sys
import os
import logging
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir) 

from api_consumer.es_client import ElasticCustomCLient
from api_consumer.api_client import Client
from processing.data_processing import Processer
from templates.base_templates import HTML_TEMPLATE
from config.auth import ELASTIC_AUTH
from email_service.sender import Sender
from rocketry import Rocketry

app = Rocketry()


@app.task("daily between Monday and Friday")
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        filename=f"{current_dir}/logs/mail_service.log"
    )
    client =  Client()
    es_client =  ElasticCustomCLient(['http://167.114.191.57:9200'], http_auth=ELASTIC_AUTH)
    processer = Processer(client, es_client)
    Sender.send_status(processer=processer)


if __name__ == "__main__":
    app.run()
    
