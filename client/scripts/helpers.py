from essentials import get_saldo, get_cliente, get_account_info, get_cartao


def html_to_fstring(html: str) -> str:
    html = html.replace("\n", "")
    return eval(f'f"""{html}"""')

def html_to_fstring_com_iterador(html: str, n: int) -> str:
    html = html.replace("\n", "")
    return eval(f'f"""{html}"""')