import pytest
from model_bakery import baker
from confraria.pessoa.models import PessoaFisica, PessoaJuridica


@pytest.fixture
def pessoa_fisica(db):
    return baker.make('pessoa.Pessoa', cnpj=None)


@pytest.fixture
def pessoa_juridica(db):
    return baker.make('pessoa.Pessoa', cnpj='05.418.904/0001-55')


def test_pessa_fisica_queryset_filter(pessoa_fisica):
    assert pessoa_fisica in PessoaFisica.objects.all()


def test_pessa_juridica_queryset_filter(pessoa_juridica):
    assert pessoa_juridica in PessoaJuridica.objects.all()


def test_pessa_fisica_nao_esta_queryset_filter(pessoa_fisica):
    assert pessoa_fisica not in PessoaJuridica.objects.all()


def test_pessa_juridica_nao_esta_queryset_filter(pessoa_juridica):
    assert pessoa_juridica not in PessoaFisica.objects.all()
