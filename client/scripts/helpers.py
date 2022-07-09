from essentials import get_saldo, get_cliente, get_account_info


def html_to_fstring(html: str) -> str:
    html = html.replace("\n", "")
    return eval(f'f"""{html}"""')