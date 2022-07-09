from src.entities.entity import Entity


class Cliente(Entity):
    def __init__(self, id: str) -> None:
        super().__init__(id)