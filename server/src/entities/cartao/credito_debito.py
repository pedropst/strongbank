
from decimal import Decimal
from server.src.entities.cartao.cartao import Cartao
from server.src.entities.conta.conta import Conta
from server.src.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError


class CartaoCreditoEDebito(Cartao):
    def __init__(self, bandeira: str, limite_total: Decimal) -> None:
        super().__init__(bandeira, limite_total)
        self.__tipo = '2'

    @property
    def tipo(self):
        return self.__tipo

    def pagar(self, valor: Decimal, conta: Conta):
        try:
            conta.usar_cartao(valor)
        except SaldoInsuficienteParaTransferenciaError as e:
            e.message = 'CONTA | Transferência não permitida: saldo insuficiente'
            raise e

    def pagar(self, valor: Decimal, parcelas: int):
        if self.limite_desbloqueado >= valor:
            
        # try:
            
        # except SaldoInsuficienteParaTransferenciaError as e:
        #     e.message = 'CONTA | Transferência não permitida: saldo insuficiente'
        #     raise e

