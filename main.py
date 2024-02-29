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
from email_service.sender import Sender


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        filename="mail_service.log"
    )
    client =  Client()
    http_auth = ('multipet', 'multipet@2022#$')
    es_client =  ElasticCustomCLient(['http://167.114.191.57:9200'], http_auth=http_auth)
    processer = Processer(client, es_client)
    Sender.send_status(processer=processer)
    