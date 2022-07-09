from decimal import Decimal

from src.entities.cartao.cartao import Cartao


class CartaoDebito(Cartao):
    def __init__(self, bandeira: str, limite_total: Decimal) -> None:
        super().__init__(bandeira, limite_total)
        self.__tipo = 'Debito'

    @property
    def tipo(self):
        return self.__tipo

    def pagar(self, valor: Decimal, conta: Conta): ## DEVO PASSAR O CARTAO COMO ARGUMENTO
        ## OU PROCURAR NO BANCO O DONO RELACIONADO, E PUXAR DE LÁ AS INFORMAÇÕES??????
        try:
            conta.usar_cartao(valor)
        except SaldoInsuficienteParaTransferenciaError as e:
            e.message = 'CONTA | Transferência não permitida: saldo insuficiente'
            raise e
