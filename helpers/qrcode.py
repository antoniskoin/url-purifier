from io import BytesIO
import qrcode
from helpers.strings import image_to_base64


def generate_qrcode(url_id: str) -> str:
    qr_code = qrcode.make(f"https://url-purifier.vercel.app/{url_id}")
    buffer = BytesIO()
    qr_code.save(buffer, format="JPEG")
    image = image_to_base64(buffer.getvalue())
    return image
