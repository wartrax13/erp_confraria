from django.contrib import admin
from .models import Produto, Categoria, Movimentacao
# Register your models here.
admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Movimentacao)

