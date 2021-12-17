from django.db import models
from confraria.produto.models import Categoria


class Evento(models.Model):
    nome = models.CharField('Nome', max_length=128)
    data = models.DateField('Data')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    movimentacao = models.OneToOneField(
        'produto.Movimentacao',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.nome

    def get_quantidade_doacao_produtos(self):
        result = {}
        produtos = self.categoria.produto_set.all()
        for produto in produtos:
            result[produto.nome] = (produto.total_saida, produto.descricao)

        return result


class DoacaoEvento(models.Model):
    pessoa = models.ForeignKey('pessoa.Pessoa', on_delete=models.PROTECT)
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    recebido = models.BooleanField(default=False)
    data_entrega = models.DateTimeField('Data de entrega', null=True, blank=True)

    class Meta:
        ordering = ['recebido']
        verbose_name = 'Doação de Evento'
        verbose_name_plural = 'Doações de Eventos'
        unique_together = ['pessoa', 'evento']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.evento.nome}'
