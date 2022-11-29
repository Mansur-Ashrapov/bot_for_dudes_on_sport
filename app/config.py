import configparser

conf = configparser.ConfigParser()
conf.read('app/configi.ini')


DATABASE_URL = str(conf.get('BASECLIENT', 'database_url'))
API_ID = str(conf.get('BASECLIENT', 'api_id'))
API_HASH = str(conf.get('BASECLIENT', 'api_hash'))
USERNAME = str(conf.get('BASECLIENT', 'username'))

ADDR = str(conf.get('BASECLIENTPROXY', 'addr'))
PORT = int(conf.get('BASECLIENTPROXY', 'port'))
LOGIN = str(conf.get('BASECLIENTPROXY', 'login'))
PASSWORD = str(conf.get('BASECLIENTPROXY', 'password'))

CLIENTS_USERNAMES = str(conf.get('CLIENTS', 'usernames')).split(',')


# API_ID = str(os.getenv('API_ID'))
# API_HASH = str(os.getenv('API_HASH'))
# USERNAME = str(os.getenv('USERNAME'))
# DATABASE_URL = str(os.getenv('DATABASE_URL'))