from django.db import models


class Evento(models.Model):
    nome = models.CharField('Nome', max_length=128)
    data = models.DateField('Data')

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
    
    def __str__(self):
        return self.nome


class DoacaoEvento(models.Model):
    pessoa = models.ForeignKey('pessoa.Pessoa', on_delete=models.PROTECT)
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    recebido = models.BooleanField(default=False)
    data_entrega = models.DateTimeField('Data de entrega', null=True, blank=True)

    class Meta:
        verbose_name = 'Doação de Evento'
        verbose_name_plural = 'Doações de Eventos'
        unique_together = ['pessoa', 'evento']
    
    def __str__(self):
        return f'{self.pessoa.nome} - {self.evento.nome}'
