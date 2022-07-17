from decimal import Decimal

from strongbank.entities.acoes_conta import AcoesConta
from strongbank.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError
from strongbank.exceptions.limite_insuficiente_error import LimiteInsuficienteError


class AcoesCartao():
    def pagar_debito(self, valor: float, conta: AcoesConta):
        """
            Método responsável pela lógica e a aprovação ou não de um pagamento
            feito por débito.
        """

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
        """
            Método responsável pela lógica e a aprovação ou não de um pagamento
            feito por crédito.
        """

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
        """
            Método responsável pela lógica de bloqueio e desbloqueio de cartão.
        """

        self.bloqueado = not(self.bloqueado)
        self.save()
