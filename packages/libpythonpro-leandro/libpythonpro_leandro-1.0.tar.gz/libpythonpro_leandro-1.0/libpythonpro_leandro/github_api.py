import requests


def buscar_avatar(usuario):
    """
    Busca o avatar de um usuário no Github
    :param usuario: str com o nome de usuario no Github
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{usuario}'
    response = requests.get(url)
    return response.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('LeandroBP'))
