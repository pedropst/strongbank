# Generated by Django 4.0.6 on 2022-07-10 17:58

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import strongbank.entities.conta
import strongbank.entities.credito_debito
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('0', 'Credito'), ('1', 'Debito'), ('2', 'Credito e Debito')], default=1, max_length=20)),
                ('dia_vencimento', models.IntegerField(choices=[(1, 'Dia 1'), (2, 'Dia 2'), (3, 'Dia 3'), (4, 'Dia 4'), (5, 'Dia 5'), (6, 'Dia 6'), (7, 'Dia 7'), (8, 'Dia 8'), (9, 'Dia 9'), (10, 'Dia 10'), (11, 'Dia 11'), (12, 'Dia 12'), (13, 'Dia 13'), (14, 'Dia 14'), (15, 'Dia 15'), (16, 'Dia 16'), (17, 'Dia 17'), (18, 'Dia 18'), (19, 'Dia 19'), (20, 'Dia 20'), (21, 'Dia 21'), (22, 'Dia 22'), (23, 'Dia 23'), (24, 'Dia 24'), (25, 'Dia 25'), (26, 'Dia 26'), (27, 'Dia 27'), (28, 'Dia 28')])),
                ('nome', models.CharField(default='', editable=False, max_length=30)),
                ('mes_validade', models.CharField(default='7', editable=False, max_length=2)),
                ('ano_validade', models.CharField(default='2030', editable=False, max_length=4)),
                ('bloqueado', models.BooleanField(default=True, editable=False)),
                ('dta_criacao', models.DateField(auto_now=True)),
                ('numeracao', models.CharField(editable=False, max_length=16)),
                ('limite_total', models.DecimalField(decimal_places=5, default=Decimal('0'), max_digits=15)),
                ('limite_disponivel', models.DecimalField(decimal_places=5, default=Decimal('0'), max_digits=15)),
                ('limite_desbloqueado', models.DecimalField(decimal_places=5, default=Decimal('0'), max_digits=15)),
                ('bandeira', models.CharField(max_length=20)),
            ],
            bases=(strongbank.entities.credito_debito.CartaoCreditoEDebito, models.Model),
        ),
        migrations.CreateModel(
            name='CartaoDadosSensiveis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvv', models.CharField(editable=False, max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('nome', models.CharField(max_length=80)),
                ('documento', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('endereco', models.CharField(max_length=100)),
                ('celular', models.CharField(max_length=14)),
                ('dta_criacao', models.DateField(auto_now=True)),
                ('tipo', models.CharField(choices=[('PF', 'Física'), ('PJ', 'Jurídica')], default='PF', max_length=2)),
                ('dono', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clientes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContaDadosSensiveis',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('saldo', models.DecimalField(decimal_places=5, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Fatura',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mes_ref', models.IntegerField()),
                ('ano_ref', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=5, default=Decimal('0'), max_digits=15)),
                ('parcial', models.DecimalField(decimal_places=5, default=Decimal('0'), max_digits=15)),
                ('dta_criacao', models.DateField(auto_now=True)),
                ('cartao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strongbank.cartao')),
            ],
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('S', 'Saque'), ('D', 'Deposito'), ('TE', 'Transferência Efetuada'), ('TR', 'Transferência Recebida'), ('C', 'Cartão'), ('PC', 'Pagamento por Cartão')], default='S', max_length=20)),
                ('dta_criacao', models.DateField(auto_now=True)),
                ('valor', models.DecimalField(decimal_places=5, max_digits=15)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strongbank.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=20)),
                ('valor', models.DecimalField(decimal_places=5, default=Decimal('0'), max_digits=15)),
                ('dta_criacao', models.DateField(auto_now=True)),
                ('fatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strongbank.fatura')),
            ],
        ),
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero', models.CharField(editable=False, max_length=6)),
                ('agencia', models.CharField(max_length=4)),
                ('dta_criacao', models.DateField(auto_now=True)),
                ('tipo', models.CharField(choices=[('P', 'Poupança'), ('C', 'Corrente')], default='P', max_length=20)),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='strongbank.cliente')),
                ('dados_sensiveis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='strongbank.contadadossensiveis')),
            ],
            bases=(strongbank.entities.conta.AcoesConta, models.Model),
        ),
        migrations.AddField(
            model_name='cartao',
            name='conta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strongbank.conta'),
        ),
        migrations.AddField(
            model_name='cartao',
            name='dados_sensiveis',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='strongbank.cartaodadossensiveis'),
        ),
    ]
