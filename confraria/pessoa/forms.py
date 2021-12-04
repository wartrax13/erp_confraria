from django import forms
from .models import PessoaFisica, PessoaJuridica, Telefone
from django.forms import inlineformset_factory


class Telefone1Form(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = [
            'numero',
        ]


TelefoneFormSet = inlineformset_factory(
    PessoaFisica,
    Telefone,
    form=Telefone1Form,
    fk_name='pessoa',
    fields=('numero',),
    extra=1
)


class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = [
            'nome',
            'cpf',
            'rg',
            'data_nascimento',
            'observacao',
            'ativo',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'cep',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.pk:
            del self.fields['ativo']

    def save(self, commit=True):
        if self.instance and not self.instance.pk:
            self.instance.criado_por = self.request_user
        self.instance.atualizado_por = self.request_user
        return super().save(commit=commit)


class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = [
            'nome',
            'razao_social',
            'responsavel',
            'cnpj',
            'observacao',
            'ativo',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'cep',
        ]

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.pk:
            del self.fields['ativo']

    def save(self, commit=True):
        if self.instance and not self.instance.pk:
            self.instance.criado_por = self.request_user
        self.instance.atualizado_por = self.request_user
        super().save(commit=commit)
