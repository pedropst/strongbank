from datetime import datetime
from decimal import *
from typing import List

from src.entities.entity import Entity
from src.entities.cliente.cliente import Cliente
from src.exceptions.saldo_insuficiente_saque_error import SaldoInsuficienteParaSaqueError
from src.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError
from src.exceptions.titular_not_found_error import TitularNotFoundError


class Conta(Entity):
    def __init__(self, id: str, titulares: List[Cliente], numero: str, agencia: str, saldo: Decimal) -> None:
        super().__init__(id)
        self.__titulares = titulares
        self.__numero = numero
        self.__agencia = agencia
        self.__saldo = saldo

    @property
    def titulares(self) -> List[Cliente]:
        return self.__titulares

    @property
    def numero(self) -> str:
        return self.__numero

    @property
    def agencia(self) -> str:
        return self.__agencia

    @property
    def saldo(self) -> str:
        return self.__saldo


## REMOVER ESSES MÉTODOS E COLOCAR NA CLASSE DE CONTA CONJUNTA
    def adicionar_titular(self, titular: Cliente) -> None:
        self.__titulares.append(titular)

    def remover_titular_por_cliente(self, titular: Cliente) -> None:
        try:
            self.__titulares.remove(titular)
        except TitularNotFoundError as e:
            e.mensagem = 'Titular não encontrado.'
            raise e

    def remover_titular_por_id(self, id_titular: str) -> None:
        titular = None
        for cliente in self.__titulares:
            if cliente.id == id_titular:
                titular = cliente
                self.__titulares.remove(titular)
        if titular is None:
            raise TitularNotFoundError('Titular não encontrado.')
######------------------------------------------------------------

    def sacar(self, quantidade: Decimal) -> None:
        if self.__saldo >= quantidade:
            self.__saldo -= quantidade
        else:
            raise SaldoInsuficienteParaSaqueError('CONTA | Saque não permitido: saldo insuficiente.')
    
    def depositar(self, quantidade: Decimal) -> None:
        self.__saldo += quantidade
    
    def transferir(self, quantidade: Decimal, destinatario: object) -> None:
        if self.__saldo >= quantidade:
            destinatario.depositar(quantidade)
            self.__saldo -= quantidade
        else:
            raise SaldoInsuficienteParaTransferenciaError('CONTA | Transferência não permitida: saldo insuficiente')

    def pagar_boleto(self, codigo: str) -> None:
        pass

    def gerar_extrato(self, data_inicial: datetime, data_final: datetime) -> None:
        pass

