from datetime import datetime
from decimal import *
from typing import List

from src.entities.conta.conta import Conta
from src.entities.cliente.cliente import Cliente
from src.exceptions.saldo_insuficiente_saque_error import SaldoInsuficienteParaSaqueError
from src.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError
from src.exceptions.titular_not_found_error import TitularNotFoundError


class ContaPoupanca(Conta):
    taxa_transferencia = Decimal(0.01)
    limite_saque_mensais = 2
    limite_transferencia_mensais = 2
    limite_extratos_mensais = 2
    rendimento = Decimal(0.015)

    def __init__(self, id: str, titulares: List[Cliente], numero: str, agencia: str, saldo: Decimal, cartao: Cartao) -> None:
        super().__init__(id, titulares, numero, agencia, saldo)
        self.data_de_criacao = datetime.today()
        self.cartao = cartao

    def render(self):
        self.__saldo *= (1 + Decimal(0.015))