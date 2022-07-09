from datetime import timedelta
from decimal import Decimal
import pytest

from src.entities.cartao.cartao import Cartao

@pytest.fixture()
def cartao():
    return Cartao('MasterCard', Decimal(5000))

def test_verificar_tipo(cartao):
    assert type(cartao) == Cartao

def test_verificar_tamanho_numero_gerado(cartao):
    assert len(cartao.numero) == 16

def test_verificar_tamanho_cvv_gerado(cartao):
    assert len(cartao.cvv) == 3

def test_verificar_se_esta_bloqueado(cartao):
    assert cartao.bloqueado is True

def test_verificar_limite_total_gerado(cartao):
    assert cartao.limite_total == Decimal(5000)

def test_verificar_limite_desbloqueado_gerado(cartao):
    assert cartao.limite_desbloqueado == Decimal(1000)

def test_verificar_limite_disponivel_gerado(cartao):
    assert cartao.limite_disponivel == Decimal(5000)

def test_verificar_vencimento_gerado(cartao):
    assert cartao.data_criacao + timedelta(days=365*8) == cartao.vencimento

def test_bloquear(cartao):
    cartao.bloquear()
    assert cartao.bloqueado == True

def test_desbloquear(cartao):
    cartao.desbloquear()
    assert cartao.bloqueado  == False

def test_desbloquear_e_bloquear(cartao):
    cartao.desbloquear()
    resultado = [cartao.bloqueado]
    cartao.bloquear()
    resultado.append(cartao.bloqueado)
    assert resultado[0] == False and resultado[1] == True


    