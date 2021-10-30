from django.urls import path
from .views import PessoaFisicaListView


urlpatterns = [
    path('fisica/list/', PessoaFisicaListView.as_view())
]