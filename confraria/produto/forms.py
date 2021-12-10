from django import forms
from .models import Produto, Movimentacao, Categoria


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
            'produtos',
            'pessoa',
            'data',
        ]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name']
