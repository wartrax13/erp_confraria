'''Script para criar linhas na tabela de cadastros de Pessoa Física'''

from django.contrib.auth.models import User
from confraria.pessoa.models import Pessoa
import openpyxl
from pathlib import Path


BASE_BACKUP = Path(__file__).resolve().parent


wb = openpyxl.load_workbook(
    filename=f'{BASE_BACKUP}/teste_cadastro.xlsx'
    )

for d in wb['Sheet1'].iter_rows(values_only=True):
    nome = str(d[0]).title()

    if d[1] is not None and len(str(d[1])) <= 9:
        rg = d[1]
        cpf = None
    else:
        cpf = d[1]
        rg = None

    if d[2] is None:
        bairro = 'Sem dado'
    else:
        bairro = str(d[2]).title()
    logradouro = str(d[3]).title()
    numero = d[4]

    if d[5] is None:
        complemento = '-'
    else:
        complemento = d[5]

    Pessoa(
        nome=nome,
        cpf=cpf,
        rg=rg,
        logradouro=logradouro,
        numero=numero,
        bairro=bairro,
        cidade='Limeira',
        estado='SP',
        atualizado_por=User(1),
        criado_por=User(1)
    ).save()
