from django import forms
from .models import Produto
# from django.forms import inlineformset_factory


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'categoria',
        ]

    # continuar
