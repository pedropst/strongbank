from django.db import models


class Cliente(models.Model):
    tipos_clientes = [('PF', 'Física'), ('PJ', 'Jurídica')]

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=80)
    documento = models.CharField(primary_key=True, max_length=14)
    # documento = models.OneToOneField(Documento, on_delete=models.CASCADE, null=True)
    endereco = models.CharField(max_length=100)
    celular = models.CharField(max_length=14)
    dta_criacao = models.DateField(auto_now=True)
    tipo = models.CharField(max_length=2, choices=tipos_clientes, default='PF')
    dono = models.OneToOneField('auth.User', related_name='clientes', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome