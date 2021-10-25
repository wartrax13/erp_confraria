from django.contrib import admin
from .models import Pessoa, Endereco, Telefone


admin.site.register(Pessoa)
admin.site.register(Endereco)
admin.site.register(Telefone)