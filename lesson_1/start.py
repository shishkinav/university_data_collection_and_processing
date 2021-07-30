from services.github_api.models import MyGitHub
from main import BASE_DIR


result_dir = BASE_DIR / 'lesson_1' / 'downloads'
result_dir.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    api = MyGitHub()
    try:
        # получаем и сохраняем публичную информацию о запрошенном пользователе
        username = api.USERNAME
        result = api.get_public_info(username)
        path_file = result_dir / f'{username}_info.json'
        with open(path_file, 'w', encoding='utf-8') as wfile:
            wfile.write(result)
        # получаем и сохраняем информацию о репозиториях по запрошенному пользователю
        result = api.repositories_list('shishkinav')
        path_file = result_dir / 'repositories.json'
        with open(path_file, 'w', encoding='utf-8') as wfile:
            wfile.write(result)
    except Exception as err:
        print(err)
