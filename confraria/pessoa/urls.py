from django.urls import path
from django.urls.conf import include
from .views import (
    PessoaFisicaCreateView, PessoaFisicaListView, PessoaFisicaUpdateView, PessoaFisicaDetailView,
    PessoaJuridicaListView, PessoaJuridicaCreateView, PessoaJuridicaUpdateView
)


urlpatterns = [
    path('fisica/', include([
        path('list/', PessoaFisicaListView.as_view(), name='pessoafisica_list'),
        path('create/', PessoaFisicaCreateView.as_view(), name='pessoafisica_form'),
        path('update/<int:pk>/', PessoaFisicaUpdateView.as_view(), name='pessoafisica_form'),
        path('detail/<int:pk>/', PessoaFisicaDetailView.as_view(), name='pessoafisica_detail'),
    ])),

    path('juridica/', include([
        path('list/', PessoaJuridicaListView.as_view(), name='pessoajuridica_list'),
        path('create/', PessoaJuridicaCreateView.as_view(), name='pessoajuridica_form'),
        path('update/<int:pk>/', PessoaJuridicaUpdateView.as_view(), name='pessoajuridica_form'),
    ])),
]
