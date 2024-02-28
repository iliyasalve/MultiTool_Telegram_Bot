import string
import random

def generate_password(length: int, is_punctuation: str) -> str:
    '''
    Returns a string containing random characters, numbers and/or special characters
    '''

    if is_punctuation == "Yes":
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for _ in range(length))
    

