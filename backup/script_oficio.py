from confraria.produto.models import Movimentacao


Movimentacao.objects.last()
# Ao rodar esse comando, irá retornar:
# Confirme o oficio que deseje alterar e a data
# >>> <Movimentacao: OFÍCIO 334 | Tipo: entrada | Data: 2023-12-10 23:06:56+00:00>

movimentacao = Movimentacao.objects.last()

movimentacao.numero_oficio
# >>> 334 ... Por exemplo

movimentacao.numero_oficio = 404  # numero do oficio que deseja

movimentacao.save()
