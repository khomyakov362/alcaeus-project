import string
import secrets


def generate_new_password() -> str:

    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(list(map(lambda _: secrets.choice(chars), range(20))))

    return password
