from django.contrib import admin
# from strongbank.models import Cliente, Conta, Cartao, Fatura, Parcela, Documento
from strongbank.models import Cliente, Conta, Cartao, Fatura, Parcela


class DocumentoAdmin(admin.ModelAdmin):
    fields = ['idcliente.nome', 'idcliente.endereco', 'idcliente.celular', 'idcliente.tipo', 'cpf', 'cnpj']

admin.site.register(Cliente)
# admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Conta)
admin.site.register(Cartao)
admin.site.register(Fatura)
admin.site.register(Parcela)
# admin.site.register(ContaDadosSensiveis)