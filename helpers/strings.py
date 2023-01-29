import base64
import random
import string
from io import BytesIO


def generate_random_string() -> str:
    letters_numbers = string.ascii_lowercase + string.digits
    random_string = "".join(random.choice(letters_numbers) for _ in range(10))
    return random_string


def image_to_base64(image) -> str:
    result = base64.b64encode(image).decode("utf-8")
    return result
