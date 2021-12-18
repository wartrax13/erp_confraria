from django.contrib import admin
from .models import Produto, Categoria, Movimentacao, MovimentacaoProduto
# Register your models here.
admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Movimentacao)
admin.site.register(MovimentacaoProduto)