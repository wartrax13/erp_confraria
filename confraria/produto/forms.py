from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

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


class BaseMovimentacaoFormSet(BaseInlineFormSet):
    def clean(self):
        qtd_total = {}
        tipo = self.forms[0].tipo
        for form in self.forms:
            try:
                qtd_total[form.cleaned_data['produto'].pk] += form.cleaned_data['quantidade']
            except KeyError:
                qtd_total[form.cleaned_data['produto'].pk] = form.cleaned_data['quantidade']
        for produto_pk, quantidade in qtd_total.items():
            produto = Produto.objects.get(pk=produto_pk)
            if tipo == TipoMovimentacaoChoices.SAIDA and produto.estoque < quantidade:
                raise ValidationError('Sem estoque para operação')


MovimentacaoFormSet = inlineformset_factory(
    Movimentacao,
    MovimentacaoProduto,
    form=MovimentacaoProdutoForm,
    formset=BaseMovimentacaoFormSet,
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
