from django import forms
from .models import PessoaFisica, PessoaJuridica, Telefone
from django.forms import inlineformset_factory


TelefoneFormSet = inlineformset_factory(PessoaFisica, Telefone, fields=('numero',))

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
