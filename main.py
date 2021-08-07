import pathlib
from configparser import ConfigParser


BASE_DIR = pathlib.Path.cwd()
config = ConfigParser()
config.read(BASE_DIR / 'conf' / 'services.conf')
GITHUB_USERNAME = config.get('github', 'GITHUB_USERNAME', fallback='your_github_login')
GITHUB_TOKEN = config.get('github', 'GITHUB_TOKEN', fallback='your_github_token')

MONGO_DATABASE_URL = config.get('mongo', 'ME_CONFIG_MONGODB_URL', fallback='your_github_token')

