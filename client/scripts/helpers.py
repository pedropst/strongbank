import base64
from pathlib import Path
from essentials import get_saldo, get_customer, get_account_info, get_cartao, get_bank_account


def html_to_fstring(html: str) -> str:
    html = html.replace("\n", "")
    return eval(f'f"""{html}"""')

def html_to_fstring_com_iterador(html: str, n: int) -> str:
    html = html.replace("\n", "")
    return eval(f'f"""{html}"""')

def img_to_bytes():
    img_bytes = Path(FR"client\resources\images\logo_baixo.png").read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_bytes1():
    img_bytes = Path(FR"client\resources\images\logo_icon.png").read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded