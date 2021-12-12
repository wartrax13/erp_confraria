from django import forms
from django.forms import inlineformset_factory

from .models import MovimentacaoProduto, Produto, Movimentacao, TipoMovimentacaoChoices, Categoria


class MovimentacaoProdutoForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoProduto
        fields = [
            'produto',
            'quantidade',
            'pessoa',
        ]

    def __init__(self, *args, **kwargs):
        self.tipo = kwargs.pop('tipo')
        super().__init__(*args, **kwargs)

    def clean_quantidade(self):
        value = self.cleaned_data['quantidade']
        if self.tipo == TipoMovimentacaoChoices.SAIDA and value > self.cleaned_data['produto'].estoque:
            self.add_error('quantidade', 'Não há estoque suficiente para a operação!')
        return value


MovimentacaoFormSet = inlineformset_factory(
    Movimentacao,
    MovimentacaoProduto,
    form=MovimentacaoProdutoForm,
    fk_name='movimentacao',
    fields=('produto', 'quantidade', 'pessoa'),
    extra=1
)


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
            'data',
        ]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name']
