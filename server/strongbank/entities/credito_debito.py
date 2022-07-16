from decimal import Decimal

from strongbank.entities.cartao import Cartao
from strongbank.entities.conta import AcoesConta
from strongbank.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError
from strongbank.exceptions.limite_insuficiente_error import LimiteInsuficienteError


class AcoesCartao():
    def pagar_debito(self, valor: float, conta: AcoesConta):
        valor = Decimal(valor)
        if not self.bloqueado:
            if conta.dados_sensiveis.saldo >= valor:
                conta.dados_sensiveis.saldo -= valor
                conta.dados_sensiveis.save()
                return True
            else:
                raise SaldoInsuficienteParaTransferenciaError({'ERRO':'CONTA | Pagamento não permitida: saldo insuficiente.'})
        else:
            raise LimiteInsuficienteError({'ERRO':'CARTÃO | Cartão está bloqueado.'})

    def pagar_credito(self, valor: float):
        valor = Decimal(valor)
        if not self.bloqueado:
            if self.limite_desbloqueado >= valor:
                self.limite_disponivel -= valor
                self.limite_desbloqueado -= valor
                self.save()
                return True
            elif self.limite_desbloqueado <= valor and self.limite_disponivel >= valor:
                raise LimiteInsuficienteError({'ERRO':'CARTÃO | Pagamento não permitido: limite DESBLOQUEADO insuficiente.'})
            elif self.limite_desbloqueado <= valor and self.limite_disponivel <= valor:
                raise LimiteInsuficienteError({'ERRO':'CARTÃO | Pagamento não permitido: limite TOTAL insuficiente.'})
        else:
            raise LimiteInsuficienteError({'ERRO':'CARTÃO | Cartão está bloqueado.'})
            
    def inverter_estado_bloqueio(self):
        self.bloqueado = not(self.bloqueado)
        self.save()
    
    # def alterar_limite(self, valor: float):
    #     valor = Decimal(valor)

    #     if valor < self.limite_total:
    #         if valor < self.limite_disponivel:
    #             if self.limite_escolhido < valor:
    #                 self.limite_desbloqueado += (valor - self.limite_escolhido)
    #             else:
    #                 self.limite_desbloqueado += (valor - self.limite_escolhido)
    #             self.limite_escolhido = valor
    #             self.save()
    #         else:
    #             raise LimiteInsuficienteError({'ERRO':'CARTÃO | Novo limite desbloqueado é menor do que o somatório das faturas.'})
    #     else:
    #         raise LimiteInsuficienteError({'ERRO':'CARTÃO | Novo limite desbloqueado é maior do que disponível.'})


        # if valor > self.limite_total:
        #     raise LimiteInsuficienteError({'ERRO':'CARTÃO | Novo limite desbloqueado é maior do que disponível.'})
        # elif valor < (self.limite_total - self.limite_disponivel):
        #     raise LimiteInsuficienteError({'ERRO':'CARTÃO | Novo limite desbloqueado é menor do que o somatório das faturas.'})
        # self.limite_desbloqueado = self.limite_total - valor
        