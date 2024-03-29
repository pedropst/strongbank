from datetime import datetime, date
from decimal import Decimal
from typing import List
import pytz

from strongbank.exceptions.saldo_insuficiente_saque_error import SaldoInsuficienteParaSaqueError
from strongbank.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError


class AcoesConta(): 
    @property
    def numero(self) -> str:
        return self.numero

    @property
    def agencia(self) -> str:
        return self.agencia

    @property
    def saldo(self) -> str:
        return self.dados_sensiveis.saldo
        
    def sacar(self, quantidade: float) -> None:
        """
            Método responsável pela lógica e a aprovação ou não de um saque.
        """

        quantidade = Decimal(quantidade)
        if self.dados_sensiveis.saldo >= quantidade:
            self.dados_sensiveis.saldo -= quantidade
            self.dados_sensiveis.save()
        else:
            raise SaldoInsuficienteParaSaqueError({'ERRO':'Saque não permitido: saldo insuficiente.'})
    
    def depositar(self, quantidade: Decimal) -> None:
        """
            Método responsável pela lógica e a aprovação ou não de um depósito.
        """

        quantidade = Decimal(quantidade)
        self.dados_sensiveis.saldo += quantidade
        self.dados_sensiveis.save()
    
    def transferir(self, quantidade: Decimal, destinatario: object) -> None:
        """
            Método responsável pela lógica e a aprovação ou não de uma transferência.
        """

        quantidade = Decimal(quantidade)
        if self.dados_sensiveis.saldo >= quantidade:
            destinatario.depositar(quantidade)
            self.sacar(quantidade)
        else:
            raise SaldoInsuficienteParaTransferenciaError({'ERRO':'Transferência não permitida: saldo insuficiente'})


    def extrato(self, dta_inicial: str, dta_final: str, transacoes: list) -> List[dict]:
        """
            Método responsável pela lógica e a aprovação ou não de um extrato.
        """

        data_inicial = datetime.strptime(dta_inicial, r'%d/%m/%Y').replace(hour=0, minute=0, second=0).astimezone(pytz.timezone('America/Sao_Paulo'))
        data_final = datetime.strptime(dta_final, r'%d/%m/%Y').replace(hour=22, minute=59, second=59).astimezone(pytz.timezone('America/Sao_Paulo'))

        # data_inicial = datetime(int(dta_inicial.split('/')[2]), int(dta_inicial.split('/')[1]), int(dta_inicial.split('/')[0]))
        # data_final = datetime(int(dta_final.split('/')[2]), int(dta_final.split('/')[1]), int(dta_final.split('/')[0]))
        transacoes_filtradas = [x for x in transacoes if (x.dta_criacao >= data_inicial and x.dta_criacao <= data_final)]
        transacoes_filtradas = sorted(transacoes_filtradas, key= lambda x: x.dta_criacao)
        extrato_gerado = {}
        tradutor = {'S':'SAQUE', 'D':'DEPÓSITO', 'T':'TRANSFERÊNCIA', 'TE':'TRANSFERÊNCIA EFETUADA', 'TR':'TRANSFERÊNCIA RECEBIDA', 'PC':'PAGAMENTO POR CARTÃO'}
        for t in transacoes_filtradas:
            t.tipo = tradutor[t.tipo]
            t.dta_criacao = datetime.strftime(t.dta_criacao, r'%d/%m/%Y %H:%M:%S')
        # for i, x in enumerate(transacoes_filtradas):
        #     extrato_gerado[i] = f'{x.dta_criacao.strftime(r"%d/%m/%Y")}: {tradutor[x.tipo]}, no valor de R${x.valor:.2f}'
        return transacoes_filtradas
