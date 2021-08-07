import pathlib
from configparser import ConfigParser


BASE_DIR = pathlib.Path.cwd()
config = ConfigParser()
config.read(BASE_DIR / 'conf' / 'services.conf')
GITHUB_USERNAME = config.get('github', 'username', fallback='your_github_login')
GITHUB_TOKEN = config.get('github', 'token', fallback='your_github_token')


if __name__ == '__main__':
    # bash -c 'python scripts/generate_env_source.py 1>.env'
    for section in config.sections():
        for option in config.options(section):
            print(f'{option.upper()}={config.get(section, option)}')
