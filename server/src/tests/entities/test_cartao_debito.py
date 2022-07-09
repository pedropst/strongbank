from datetime import timedelta
from decimal import Decimal
import pytest

from src.entities.cartao.debito import CartaoDebito
from src.entities.conta.conta import Conta

@pytest.fixture()
def cartao():
    return CartaoDebito('MasterCard', Decimal(5000))

def test_verificar_limite_total_gerado(cartao):
    assert cartao.tipo == 'Debito'