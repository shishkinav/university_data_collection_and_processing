import pathlib
from configparser import ConfigParser


BASE_DIR = pathlib.Path.cwd()
config = ConfigParser()
config.read(BASE_DIR / 'conf' / 'services.conf')
GITHUB_USERNAME = config.get('github', 'username', fallback='your_github_login')
GITHUB_TOKEN = config.get('github', 'token', fallback='your_github_token')

