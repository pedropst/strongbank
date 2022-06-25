from src.entities.entity import Entity

class Cliente(Entity):
    def __init__(self, id: str, nome: str, endereco: str, telefone: str) -> None:
        super().__init__(id)
        self.__nome = nome
        self.__endereco = endereco
        self.__telefone = telefone
    
    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def endereco(self) -> str:
        return self.__endereco

    @property
    def telefone(self) -> str:
        return self.__telefone
