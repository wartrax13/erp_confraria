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
        super().__init__(*args, **kwargs)
