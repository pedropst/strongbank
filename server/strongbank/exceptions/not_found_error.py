from src.exceptions.base_conta_error import BaseContaError

class NotFoundError(BaseContaError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)