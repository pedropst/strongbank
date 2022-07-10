# from datetime import datetime, timedelta
# from decimal import Decimal
# import os
# from random import randint
# from django.db import models
# # from django_cryptography.fields import encrypt
# from django.core.signing import Signer
# import uuid

# from strongbank.entities.conta import AcoesConta
# from strongbank.entities.credito_debito import CartaoCreditoEDebito

# class Cliente(models.Model):
#     tipos_clientes = [('PF', 'Física'), ('PJ', 'Jurídica')]

#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     nome = models.CharField(max_length=80)
#     documento = models.CharField(primary_key=True, max_length=14)
#     # documento = models.OneToOneField(Documento, on_delete=models.CASCADE, null=True)
#     endereco = models.CharField(max_length=100)
#     celular = models.CharField(max_length=14)
#     dta_criacao = models.DateField(auto_now=True)
#     tipo = models.CharField(max_length=2, choices=tipos_clientes, default='PF')
#     dono = models.OneToOneField('auth.User', related_name='clientes', on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.nome

# class ContaDadosSensiveis(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     saldo = models.DecimalField(max_digits=15, decimal_places=5)
#     # saldo = models.CharField(max_length=200)

#     def save(self, *args, **kwargs):
#         signer = Signer()
#         # self.idconta = signer.sign(self.idconta)
#         # saldo = Decimal(self.saldo)
#         # self.saldo = signer.sign(self.saldo)
#         super().save(*args, **kwargs)
 
# class Conta(AcoesConta, models.Model):
#     conta_tipo = [('P', 'Poupança'), ('C', 'Corrente')]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
#     numero = models.CharField(max_length=6, editable=False)
#     agencia = models.CharField(max_length=4)
#     dta_criacao = models.DateField(auto_now=True)
#     dados_sensiveis = models.OneToOneField(ContaDadosSensiveis, on_delete=models.CASCADE)
#     tipo = models.CharField(max_length=20, choices=conta_tipo, default=conta_tipo[0][0])
#     # dados = ContaDadosSensiveis()
#     # dados.saldo += 50

#     def save(self, *args, **kwargs):
#         todos_numeros = [x.numero for x in list(Conta.objects.all())]
#         while self.numero in todos_numeros:
#             self.numero = str(randint(10**5, (10**6)-1))
#         super().save(*args, **kwargs)

#     def __str__(self) -> str:
#         return self.cliente.nome

# class Transacao(models.Model):
#     acoes_tipo = [('S','Saque'), ('D','Deposito'), ('TE','Transferência Efetuada'), ('TR','Transferência Recebida'), ('C','Cartão'), ('PC', 'Pagamento por Cartão')]
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     # cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, unique=False)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     tipo = models.CharField(max_length=20, choices=acoes_tipo, default=acoes_tipo[0][0])
#     dta_criacao = models.DateField(auto_now=True)
#     valor = models.DecimalField(max_digits=15, decimal_places=5)

#     def save(self, *args, **kwargs):
#         if self.tipo in ['S', 'T', 'C']:
#             self.valor = Decimal(self.valor) * Decimal(-1)
#         super().save(*args, **kwargs)

#     def __str__(self) -> str:
#         return f'{self.tipo} -> {self.valor}'

# class CartaoDadosSensiveis(models.Model):
#     cvv = models.CharField(max_length=3, editable=False)

#     # def save(self, *args, **kwargs):
#     #     self.cvv = encrypt(self.cvv, os.getenv('SECRET_KET'))
#     #     super().save(*args, **kwargs)


# class Cartao(CartaoCreditoEDebito, models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
#     tipo = models.CharField(max_length=20, choices=[('0', 'Credito'), 
#                        ('1', 'Debito'), ('2', 'Credito e Debito')], 
#                        default=1)
#     dia_vencimento = models.IntegerField(choices=[(x+1, f'Dia {x+1}') for x in range(28)])
#     nome = models.CharField(max_length=30, editable=False, default='')
#     mes_validade = models.CharField(max_length=2, editable=False, default=str(datetime.today().month))
#     ano_validade = models.CharField(max_length=4, editable=False, default=str(datetime.today().year + 8))
#     bloqueado = models.BooleanField(editable=False, default=True)
#     dta_criacao = models.DateField(auto_now=True)
#     numeracao = models.CharField(max_length=16, editable=False)
#     dados_sensiveis = models.OneToOneField(CartaoDadosSensiveis, on_delete=models.CASCADE)
#     limite_total = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
#     limite_disponivel = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
#     limite_desbloqueado = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
#     bandeira = models.CharField(max_length=20)
    
#     def __str__(self) -> str:
#         return self.nome
    

# class Fatura(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE)
#     mes_ref = models.IntegerField()
#     ano_ref = models.IntegerField()
#     total = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
#     parcial = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
#     dta_criacao = models.DateField(auto_now=True)

#     def criar_vencimento(self):
#         self.mes_ref = (datetime.today() + timedelta(days=31)).date().month
#         self.ano_ref = (datetime.today() + timedelta(days=31)).date().year

#     def __str__(self) -> str:
#         return str(self.mes_ref).zfill(2)+str(self.ano_ref)
    
# class Parcela(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE)
#     descricao = models.CharField(max_length=20, editable=True)
#     valor = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
#     dta_criacao = models.DateField(auto_now=True)

#     def __str__(self) -> str:
#         return self.descricao