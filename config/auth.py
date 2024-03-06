import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = 'http://multipetcloud.com.br/api/devices/'
BASE_URL_ISSUE = 'https://multipetcloud.com.br/api/issue-inspections/'

# AUTH =('ojaomarco', 'Jo@o1501')
# ELASTIC_AUTH = ('multipet', 'multipet@2022#$')

# SENDER = "multipetmcloud.noreply@gmail.com"
# PASSWORD = "terf fcom bfii tkyj"
# text = "Multipet Sopradoras"

AUTH =(os.getenv('MCLOUD_USER'), os.getenv('MCLOUD_PWD'))
ELASTIC_AUTH = (os.getenv('ELASTIC_USER'), os.getenv('ELASTIC_PWD'))

SENDER = os.getenv('MAIL_USER')
PASSWORD = os.getenv('MAIL_PWD')