from django.db import models
from django.db.models import Sum
from django.db.models import Max


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
        if self.descricao:
            return f'{self.nome} ({self.descricao[:15]})'
        return self.nome

    @property
    def total_entrada(self):
        return self.movimentacao_set.filter(
            tipo=TipoMovimentacaoChoices.ENTRADA
        ).aggregate(total=Sum('movimentacaoproduto__quantidade')).get('total') or 0

    @property
    def total_saida(self):
        return self.movimentacao_set.filter(
            tipo=TipoMovimentacaoChoices.SAIDA
        ).aggregate(total=Sum('movimentacaoproduto__quantidade')).get('total') or 0

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
    data = models.DateTimeField()
    observacao = models.TextField(blank=True, null=True, verbose_name='Observações')
    numero_oficio = models.IntegerField(blank=True, null=True, unique=True)
    produtos = models.ManyToManyField(
        Produto,
        through='MovimentacaoProduto',
        through_fields=('movimentacao', 'produto'),
    )

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.numero_oficio = Movimentacao.objects.aggregate(Max('numero_oficio'))['numero_oficio__max'] + 1
        super(Movimentacao, self).save(*args, **kwargs)

    @property
    def quantidade(self):
        return self.produtos.aggregate(total=Sum('movimentacaoproduto__quantidade')).get('total') or 0

    @property
    def pessoas_envolvidas(self):
        return self.movimentacaoproduto_set.order_by(
            'pessoa__nome'
        ).distinct().values_list('pessoa__nome', flat=True)

    @property
    def produtos_envolvidos(self):
        return self.movimentacaoproduto_set.order_by(
            'produto__nome'
        ).distinct().values_list('produto__nome', flat=True)

    def __str__(self):
        return 'OFÍCIO {} | Tipo: {} | Data: {}'.format(
            self.numero_oficio,
            self.tipo,
            self.data
        )


class MovimentacaoProduto(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    pessoa = models.ForeignKey('pessoa.Pessoa', on_delete=models.PROTECT)
    quantidade = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'OFÍCIO {} | {} para {} | QTD: {}'.format(
            self.movimentacao.numero_oficio,
            self.produto,
            self.pessoa,
            self.quantidade
        )
