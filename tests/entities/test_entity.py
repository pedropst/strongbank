from src.entities.entity import Entity

def test_criar_entitidade():
    id = '10'
    entidade = Entity(id)

    assert type(entidade) == Entity

def test_verificar_se_id_eh_o_criado():
    id = '11'
    entidade = Entity(id)

    assert entidade.id == id

