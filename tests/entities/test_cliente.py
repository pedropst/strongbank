import pytest

from src.entities.cliente.cliente import Cliente


@pytest.fixture()
def cliente():
    return Cliente('1', 'Pedro', 'Rua do moradores bonitos, 274', '5567999999999')

def test_verificar_tipo(cliente):
    assert type(cliente) == Cliente

def test_verificar_id_criado(cliente):
    assert cliente.id == '1'

def test_verificar_nome_criado(cliente):
    assert cliente.nome == 'Pedro'
    
def test_verificar_endereco_criado(cliente):
    assert cliente.endereco == 'Rua do moradores bonitos, 274'

def test_verificar_telefone_criado(cliente):
    assert cliente.telefone == '5567999999999'

def test_tipo_id_criado(cliente):
    assert type(cliente.id) == str

def test_tipo_nome_criado(cliente):
    assert type(cliente.nome) == str

def test_tipo_endereco_criado(cliente):
    assert type(cliente.endereco) == str

def test_tipo_telefone_criado(cliente):
    assert type(cliente.telefone) == str
