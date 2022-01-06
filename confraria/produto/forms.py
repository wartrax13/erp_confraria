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
        self.fields['pessoa'].queryset = self.fields['pessoa'].queryset.order_by('nome')

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
            produto = form.cleaned_data.get('produto')
            quantidade = form.cleaned_data.get('quantidade')
            pessoa = form.cleaned_data.get('pessoa') or self.forms[0].cleaned_data.get('pessoa')
            if not pessoa:
                form.add_error('pessoa', 'Pessoa é obrigatória')
            if produto and quantidade:
                try:
                    qtd_total[produto.pk] += quantidade
                except KeyError:
                    qtd_total[produto.pk] = quantidade
            else:
                if not produto:
                    form.add_error('produto', 'Produto é obrigatório')
                if not quantidade:
                    form.add_error('quantidade', 'Quantidade é obrigatória')
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
            'observacao',
        ]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name']
