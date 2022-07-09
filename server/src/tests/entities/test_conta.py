from decimal import *
from statistics import quantiles
from typing import List
import pytest

from src.entities.cliente.cliente import Cliente
from src.entities.conta.conta import Conta
from src.exceptions.saldo_insuficiente_saque_error import SaldoInsuficienteParaSaqueError
from src.exceptions.saldo_insuficiente_transferencia_error import SaldoInsuficienteParaTransferenciaError
from src.exceptions.titular_not_found_error import TitularNotFoundError


@pytest.fixture()
def conta():
    cliente = Cliente('1', 'Pedro', 'Rua do moradores bonitos, 270', '5567999999999')
    return Conta('2', [cliente], '963226', '0001', Decimal(50))

def test_tipo_criado(conta):
    assert type(conta) == Conta


# ATRIBUTES TESTS
def test_verificar_id_criado(conta):
    assert conta.id == '2'

def test_verificar_titulares_criado(conta):
    cliente = Cliente('1', 'Pedro', 'Rua do moradores bonitos, 270', '5567999999999')
    assert conta.titulares[0].id == cliente.id
    
def test_verificar_numero_criado(conta):
    assert conta.numero == '963226'

def test_verificar_agencia_criado(conta):
    assert conta.agencia == '0001'

def test_verificar_saldo_criado(conta):
    assert conta.saldo == Decimal(50)


# ATRIBUTES' TYPE TESTS
def test_tipo_id_criado(conta):
    assert type(conta.id) == str

def test_tipo_titulares_criado(conta):
    assert type(conta.titulares) == list

def test_tipo_numero_criado(conta):
    assert type(conta.numero) == str

def test_tipo_agencia_criado(conta):
    assert type(conta.agencia) == str

def test_tipo_saldo_criado(conta):
    assert type(conta.saldo) == Decimal

# METHODS TESTS
def test_sacar_qnt_sacavel(conta):
    quantidade = 10
    conta.sacar(Decimal(quantidade))
    assert conta.saldo == Decimal(40)

def test_sacar_qnt_nao_sacavel(conta):
    quantidade = 60
    with pytest.raises(SaldoInsuficienteParaSaqueError):
        conta.sacar(Decimal(quantidade))

def test_depositar(conta):
    quantidade = Decimal(60)
    conta.depositar(quantidade)
    assert conta.saldo == Decimal(110)

def test_transferir(conta):
    quantidade = Decimal(40)
    cliente = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    conta1 = Conta('3', [cliente], '15651', '0001', Decimal(100))
    
    conta.transferir(quantidade, conta1)

    assert conta1.saldo == Decimal(140)

def test_transferir_com_saldo_insuficiente(conta):
    quantidade = Decimal(60)
    cliente = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    conta1 = Conta('3', [cliente], '15651', '0001', Decimal(100))
    
    with pytest.raises(SaldoInsuficienteParaTransferenciaError):
        conta.transferir(quantidade, conta1)


def test_adicionar_titular(conta):
    cliente2 = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    conta.adicionar_titular(cliente2)
    assert conta.titulares[1].id == cliente2.id

def test_verificar_se_adicionar_titular_aumenta_a_qnt_de_titulares(conta):
    cliente2 = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    conta.adicionar_titular(cliente2)
    assert len(conta.titulares) == 2

def test_remover_titular_por_cliente(conta):
    cliente2 = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    conta.adicionar_titular(cliente2)
    conta.remover_titular_por_cliente(cliente2)
    assert len(conta.titulares) == 1

def test_remover_titular_por_id(conta):
    cliente2 = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    conta.adicionar_titular(cliente2)
    conta.remover_titular_por_id(cliente2.id)
    assert len(conta.titulares) == 1

def test_remover_titular_inexiste_por_cliente(conta):
    cliente2 = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    with pytest.raises(TitularNotFoundError):
        conta.remover_titular_por_id(cliente2)

def test_remover_titular_inexiste_por_id(conta):
    cliente2 = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    with pytest.raises(TitularNotFoundError):
        conta.remover_titular_por_id(cliente2.id)


# ALTERNATIVE TESTS
def test_qnt_de_titulares():
    cliente1 = Cliente('1', 'Pedro', 'Rua do moradores bonitos, 270', '5567999999999')
    cliente2 = Cliente('2', 'Bianca', 'Rua do moradores bonitos, 274', '5567999996666')
    conta = Conta('3', [cliente1, cliente2], '963226', '0001', Decimal(50))

    assert len(conta.titulares) == 2
