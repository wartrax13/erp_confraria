from django.urls import path
from django.urls.conf import include
from .views import (
    PessoaFisicaCreateView, PessoaFisicaListView,
    PessoaJuridicaListView, PessoaFisicaUpdateView
)


urlpatterns = [
    path('fisica/', include([
        path('list/', PessoaFisicaListView.as_view(), name='pessoafisica_list'),
        path('create/', PessoaFisicaCreateView.as_view(), name='pessoafisica_form'),
        path('update/<int:pk>/', PessoaFisicaUpdateView.as_view(), name='pessoafisica_form'),
    ])),

    path('juridica/', include([
        path('list/', PessoaJuridicaListView.as_view(), name='pessoajuridica_list'),
    ])),
]