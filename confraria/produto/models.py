from django.db import models
from django.db.models import Sum


class TipoMovimentacaoChoices(models.TextChoices):
    ENTRADA = 'entrada', 'Entrada'
    SAIDA = 'saida', 'Saída'


class Categoria(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)  # de um para muitos
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome

    @property
    def total_entrada(self):
        return self.movimentacao_set.filter(
            tipo=TipoMovimentacaoChoices.ENTRADA
        ).aggregate(total=Sum('quantidade')).get('total') or 0

    @property
    def total_saida(self):
        return self.movimentacao_set.filter(
            tipo=TipoMovimentacaoChoices.SAIDA
        ).aggregate(total=Sum('quantidade')).get('total') or 0

    @property
    def estoque(self):
        return self.total_entrada - self.total_saida
    
    @property
    def disponibilidade(self):
        if self.estoque < 1:
            return False
        return True


class Movimentacao(models.Model):
    tipo = models.CharField('Tipo', max_length=128, choices=TipoMovimentacaoChoices.choices)
    quantidade = models.PositiveIntegerField()
    produto = models.ForeignKey('produto.Produto', on_delete=models.PROTECT)
    pessoa = models.ForeignKey('pessoa.Pessoa', on_delete=models.PROTECT)
    data = models.DateTimeField()

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
