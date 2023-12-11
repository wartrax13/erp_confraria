
import datetime

from confraria.evento.models import DoacaoEvento, Evento
from confraria.produto.models import Categoria


categoria = Categoria.objects.get_or_create(name='Natal 2023')
original_evento = Evento.objects.last()

novo_evento = Evento.objects.create(
    nome='Evento - Doações de Cestas Básicas Natal 2023 - Oxalá',
    data=datetime.date(2023, 12, 19),
    categoria=categoria
)

# Duplicar as DoacaoEvento relacionadas ao Evento
for doacao_evento in original_evento.doacaoevento_set.all():
    DoacaoEvento.objects.create(
        pessoa=doacao_evento.pessoa,
        evento=novo_evento
    )
