import base64
from tempfile import SpooledTemporaryFile


def convert_file_to_html_base64(file: SpooledTemporaryFile) -> bytes:
    file.seek(0)
    img_as_base64 = base64.b64encode(file.read())
    return b"data:image/png;base64, " + img_as_base64
