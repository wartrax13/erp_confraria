from django.db import models
from django.db.models.deletion import CASCADE, PROTECT


class EstadoChoices(models.TextChoices):
    AC = 'AC', 'Acre'
    AL = 'AL', 'Alagoas'
    AP = 'AP', 'Amapá'
    AM = 'AM', 'Amazonas'
    BA = 'BA', 'Bahia'
    CE = 'CE', 'Ceará'
    DF = 'DF', 'Distrito Federal'
    ES = 'ES', 'Espírito Santo'
    GO = 'GO', 'Goiás'
    MA = 'MA', 'Maranhão'
    MT = 'MT', 'Mato Grosso'
    MS = 'MS', 'Mato Grosso do Sul'
    MG = 'MG', 'Minas Gerais'
    PA = 'PA', 'Pará'
    PB = 'PB', 'Paraíba'
    PR = 'PR', 'Paraná'
    PE = 'PE', 'Pernambuco'
    PI = 'PI', 'Piauí'
    RJ = 'RJ', 'Rio de Janeiro'
    RN = 'RN', 'Rio Grande do Norte'
    RS = 'RS', 'Rio Grande do Sul'
    RO = 'RO', 'Rondônia'
    RR = 'RR', 'Rorâima'
    SC = 'SC', 'Rio Grande do Sul'
    SP = 'SP', 'São Paulo'
    SE = 'SP', 'Sergipe'
    TO = 'TO', 'Tocantins'


class Endereco(models.Model):
    logradouro = models.CharField('Logradouro', max_length=128, null=True, blank=True)
    numero = models.CharField('Número', max_length=8, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=128, null=True, blank=True)
    complemento = models.CharField('Complemento', max_length=128, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=128, null=True, blank=True)
    estado = models.CharField('Estado', choices=EstadoChoices.choices, null=True, blank=True)
    cep = models.CharField('CEP', max_length=9, null=True, blank=True)
    
    class Meta:
        verbose_name = ('Endereço',)
        verbose_name_plural = ('Endereços')

    def __str__(self):
        return self.numero  


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=128, null=True, blank=True)
    razao_social = models.CharField('RAzão Social', max_length=128, null=True, blank=True)
    responsavel = models.CharField('Responsável', max_length=128, null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=18, null=True, blank=True, unique=True)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True, unique=True)
    rg = models.CharField('RG', max_length=12, null=True, blank=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    endereco = models.ForeignKey('Endereço', on_delete=PROTECT, null=True, blank=True)
    observacao = models.TextField('Observação', max_length=128, null=True, blanck=True)
    ativo = models.BooleanField('Ativo', default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Pessoa',)
        verbose_name_plural = ('Pessoas')

    def __str__(self):
        return self.nome


class Telefone(models.Model):
    numero = models.CharField('Telefone', max_length=128, null=True, blank=True)
    pessoa = models.ForeignKey('Pessoa', on_delete=CASCADE, related_name='pessoas')

    class Meta:
        verbose_name = ('Telefone',)
        verbose_name_plural = ('Telefones')

    def __str__(self):
        return self.numero