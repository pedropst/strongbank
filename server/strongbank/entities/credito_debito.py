from decimal import Decimal

from strongbank.entities.cartao import Cartao
from strongbank.entities.conta import AcoesConta
from strongbank.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError
from strongbank.exceptions.limite_insuficiente_error import LimiteInsuficienteError


class AcoesCartao():
    @property
    def numero(self):
        return self.__numero

    @property
    def bandeira(self):
        return self.__bandeira

    @property
    def data_criacao(self):
        return self.__data_criacao
        
    @property
    def vencimento(self):
        return self.__vencimento

    @property
    def cvv(self):
        return self.__cvv

    @property
    def bloqueado(self):
        return self.__bloqueado

    @property
    def limite_total(self):
        return self.__limite_total

    @property
    def limite_desbloqueado(self):
        return self.__limite_desbloqueado

    @property
    def limite_disponivel(self):
        return self.__limite_disponivel

    @property
    def tipo(self):
        return self.__tipo

    def pagar_debito(self, valor: float, conta: AcoesConta):
        valor = Decimal(valor)
        if conta.dados_sensiveis.saldo >= valor:
            conta.dados_sensiveis.saldo -= valor
            conta.dados_sensiveis.save()
            return True
        else:
            raise SaldoInsuficienteParaTransferenciaError({'ERRO':'CONTA | Pagamento não permitida: saldo insuficiente.'})


    def pagar_credito(self, valor: float):
        valor = Decimal(valor)
        if self.limite_desbloqueado >= valor:
            self.limite_disponivel -= valor
            self.limite_desbloqueado -= valor
            self.save()
            return True
        else:
            raise LimiteInsuficienteError({'ERRO':'CARTÃO | Pagamento não permitido: limite insuficiente.'})
