import configparser

conf = configparser.ConfigParser()
conf.read('app/configi.ini')


DATABASE_URL=str(conf.get('INITIALIZE', 'database_url'))
API_ID=str(conf.get('INITIALIZE', 'api_id'))
API_HASH=str(conf.get('INITIALIZE', 'api_hash'))
USERNAME=str(conf.get('INITIALIZE', 'username'))


# API_ID = str(os.getenv('API_ID'))
# API_HASH = str(os.getenv('API_HASH'))
# USERNAME = str(os.getenv('USERNAME'))
# DATABASE_URL = str(os.getenv('DATABASE_URL'))