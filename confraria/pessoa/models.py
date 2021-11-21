from django.db import models
from django.conf import settings


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
    SE = 'SE', 'Sergipe'
    TO = 'TO', 'Tocantins'


class BaseModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_criadas",
    )
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_atualizadas",
    )
    class Meta:
        abstract = True


class Pessoa(BaseModel):
    nome = models.CharField('Nome', max_length=128)
    razao_social = models.CharField('Razão Social', max_length=128, null=True, blank=True)
    responsavel = models.CharField('Responsável', max_length=128, null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=18, null=True, blank=True, unique=True)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True, unique=True)
    rg = models.CharField('RG', max_length=12, null=True, blank=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    observacao = models.TextField('Observação', max_length=128, null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)

    # Endereco
    logradouro = models.CharField('Logradouro', max_length=128, null=True, blank=True)
    numero = models.CharField('Número', max_length=8, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=128)
    complemento = models.CharField('Complemento', max_length=128, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=128)
    estado = models.CharField('Estado', max_length=2, choices=EstadoChoices.choices)
    cep = models.CharField('CEP', max_length=9, null=True, blank=True)
    

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.nome


class PessoaFisicaManager(models.Manager):
    """
    Filtra os objetos que retornam de uma queryset. 
    Os dados que não tiverem CNPJ, são PF.
    """
    def get_queryset(self):
        return super().get_queryset().exclude(cnpj__isnull=False)


class PessoaFisica(Pessoa):
    objects = PessoaFisicaManager()

    class Meta:
        proxy = True # É usado como referencia de Pessoa (sem criar uma tabela no banco de dados)
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'


class PessoaJuridicaManager(models.Manager):
    """
    Filtra os objetos que retornam de uma queryset. 
    Os dados que tiverem CNPJ, são PJ.
    """
    def get_queryset(self):
        return super().get_queryset().filter(cnpj__isnull=False)


class PessoaJuridica(Pessoa):
    objects = PessoaJuridicaManager()

    class Meta:
        proxy = True # É usado como referencia de Pessoa (sem criar uma tabela no banco de dados)
        verbose_name = 'Pessoa Jurídica'
        verbose_name_plural = 'Pessoas Jurídicas'


class Telefone(models.Model):
    numero = models.CharField('Telefone', max_length=128, null=True, blank=True)
    principal = models.BooleanField('Principal', default=False)
    pessoa = models.ForeignKey('Pessoa', on_delete=models.CASCADE, related_name='pessoas')

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'

    def __str__(self):
        return self.numero
