from rest_framework import serializers

class BaseContaError(serializers.ValidationError):
    def __init__(self, *args: object) -> None:
        self.mensagem = args[0]
        super().__init__(*args)