from decimal import Decimal

from src.entities.cartao.cartao import Cartao
from src.entities.conta.conta import Conta
from src.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError


class CartaoDebito(Cartao):
    def __init__(self, bandeira: str, limite_total: Decimal) -> None:
        super().__init__(bandeira, limite_total)
        self.__tipo = 'Debito'

    @property
    def tipo(self):
        return self.__tipo

    def pagar(self, valor: Decimal, conta: Conta):
        try:
            conta.usar_cartao(valor)
        except SaldoInsuficienteParaTransferenciaError as e:
            e.message = 'CONTA | Transferência não permitida: saldo insuficiente'
            raise e
