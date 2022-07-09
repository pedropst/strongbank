class Entity():
    def __init__(self, id: str) -> None:
        self.__id: str = id
    
    @property
    def id(self) -> str:
        return self.__id