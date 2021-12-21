from django.contrib import admin
from .models import Produto, Categoria, Movimentacao, MovimentacaoProduto


admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Movimentacao)
admin.site.register(MovimentacaoProduto)
