from src.exceptions.saldo_insuficiente_error import SaldoInsuficienteError

class SaldoInsuficienteParaSaqueError(SaldoInsuficienteError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)