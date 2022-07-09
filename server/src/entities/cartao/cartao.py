from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from decimal import Decimal
from random import randint

class Cartao(ABC):
    def __init__(self, bandeira: str, limite_total: Decimal) -> None:
        self.__bandeira = bandeira
        if self.__bandeira is 'MasterCard':
            self.__numero: str = '5431' + str(randint(10**11, (10**12)-1))
        else:
            self.__numero: str = '1653' + str(randint(10**11, (10**12)-1))
        self.__data_criacao: datetime = datetime.today()
        self.__vencimento: datetime = (self.data_criacao + timedelta(days=365*8))
        self.__cvv: str = str(randint(10**2, (10**3)-1))
        self.__bloqueado: bool = True
        self.__limite_total: Decimal = limite_total
        self.__limite_desbloqueado: Decimal = 1000
        self.__limite_disponivel: Decimal = limite_total

        # self.__faturas = [] ## usar o hasattr() para criar na hora de gerar primeira fatura

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

    @abstractmethod
    def pagar(self):
        pass

    def bloquear(self):
        self.__bloqueado = True

    def desbloquear(self):
        self.__bloqueado = False

