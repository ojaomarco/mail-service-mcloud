import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = 'http://multipetcloud.com.br/api/devices/'
BASE_URL_ISSUE = 'https://multipetcloud.com.br/api/issue-inspections/'

AUTH =(os.getenv('MCLOUD_USER'), os.getenv('MCLOUD_PWD'))
ELASTIC_AUTH = (os.getenv('ELASTIC_USER'), os.getenv('ELASTIC_PWD'))

SENDER = os.getenv('MAIL_USER')
PASSWORD = os.getenv('MAIL_PWD')