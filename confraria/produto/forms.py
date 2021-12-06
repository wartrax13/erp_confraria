from django import forms
from .models import Produto, Movimentacao


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'categoria',
        ]
    # continuar


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = [
            'tipo',
            'quantidade',
            'produto',
            'pessoa',
            'data',
        ]
