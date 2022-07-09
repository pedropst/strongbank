from src.exceptions.saldo_insuficiente_error import SaldoInsuficienteError


class SaldoInsuficienteParaTransferenciaError(SaldoInsuficienteError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

