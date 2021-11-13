from django import forms
from .models import PessoaFisica, PessoaJuridica


class PessoaFisicaForm(forms.ModelForm):

    class Meta:
        model = PessoaFisica
        fields = [
            'nome',  
            'cpf', 
            'rg', 
            'data_nascimento',
            'observacao', 
            'ativo'
        ]
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.instance and not self.instance.pk:
            self.instance.criado_por = self.request_user

        self.instance.atualizado_por = self.request_user

        super().save(commit=commit)