# Generated by Django 3.2.8 on 2021-11-21 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=128, verbose_name='Nome')),
                ('razao_social', models.CharField(blank=True, max_length=128, null=True, verbose_name='Razão Social')),
                ('responsavel', models.CharField(blank=True, max_length=128, null=True, verbose_name='Responsável')),
                ('cnpj', models.CharField(blank=True, max_length=18, null=True, unique=True, verbose_name='CNPJ')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=12, null=True, verbose_name='RG')),
                ('data_nascimento', models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')),
                ('observacao', models.TextField(blank=True, max_length=128, null=True, verbose_name='Observação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('logradouro', models.CharField(blank=True, max_length=128, null=True, verbose_name='Logradouro')),
                ('numero', models.CharField(blank=True, max_length=8, null=True, verbose_name='Número')),
                ('bairro', models.CharField(max_length=128, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=128, null=True, verbose_name='Complemento')),
                ('cidade', models.CharField(max_length=128, verbose_name='Cidade')),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Rorâima'), ('SC', 'Rio Grande do Sul'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP')),
                ('atualizado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pessoa_pessoa_atualizadas', to=settings.AUTH_USER_MODEL)),
                ('criado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pessoa_pessoa_criadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pessoa',
                'verbose_name_plural': 'Pessoas',
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, max_length=128, null=True, verbose_name='Telefone')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pessoas', to='pessoa.pessoa')),
            ],
            options={
                'verbose_name': 'Telefone',
                'verbose_name_plural': 'Telefones',
            },
        ),
        migrations.CreateModel(
            name='PessoaFisica',
            fields=[
            ],
            options={
                'verbose_name': 'Pessoa Física',
                'verbose_name_plural': 'Pessoas Físicas',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pessoa.pessoa',),
        ),
        migrations.CreateModel(
            name='PessoaJuridica',
            fields=[
            ],
            options={
                'verbose_name': 'Pessoa Jurídica',
                'verbose_name_plural': 'Pessoas Jurídicas',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pessoa.pessoa',),
        ),
    ]
