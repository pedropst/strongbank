from src.exceptions.base_conta_error import BaseContaError

class SaldoInsuficienteError(BaseContaError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
