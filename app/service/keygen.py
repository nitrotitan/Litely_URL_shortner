import string

from app.service import key_generator


def generate_key(url):
    return key_generator.generate_key(str(url))
