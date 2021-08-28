import pathlib
from configparser import ConfigParser


BASE_DIR = pathlib.Path.cwd()
config = ConfigParser()
config.read(BASE_DIR / 'conf' / 'services.conf')

DEBUG = config.getboolean('DEFAULT', 'DEBUG', fallback=False)

GITHUB_USERNAME = config.get('github', 'username', fallback='your_github_login')
GITHUB_TOKEN = config.get('github', 'token', fallback='your_github_token')

MONGO_DATABASE_URL = config.get('mongo', 'ME_CONFIG_MONGODB_URL', fallback='your_github_token')

SCRAPY_USE_LOG = config.getboolean('scrapy', 'USE_LOG', fallback=False)
SCRAPY_LOG_LEVEL = config.get('scrapy', 'LOG_LEVEL', fallback='DEBUG')
SCRAPY_LOG_PATH = config.get('scrapy', 'LOG_PATH', fallback=BASE_DIR / 'logs' / 'scrapy.log')
INSTAGRAM_LOGIN = config.get('scrapy', 'INSTAGRAM_LOGIN', fallback='')
INSTAGRAM_HASH_PASSWORD = config.get('scrapy', 'INSTAGRAM_HASH_PASSWORD', fallback='')
INSTAGRAM_HASH_POSTS = config.get('scrapy', 'INSTAGRAM_HASH_POSTS', fallback='')
