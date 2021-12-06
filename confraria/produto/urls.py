from django.urls import path, include
from .views import (
  ProdutoListView, ProdutoCreateView, ProdutoUpdateView,
  MovimentacaoListView, MovimentacaoCreateView, MovimentacaoDetailView
  )

urlpatterns = [
    path('list/', ProdutoListView.as_view(), name='produto_list'),
    path('create/', ProdutoCreateView.as_view(), name='produto_form'),
    path('update/<int:pk>/', ProdutoUpdateView.as_view(), name='produto_form'),
    path('movimentacao/', include([
        path('list/', MovimentacaoListView.as_view(), name='movimentacao_list'),
        path('create/', MovimentacaoCreateView.as_view(), name='movimentacao_form'),
        path('detail/<int:pk>', MovimentacaoDetailView.as_view(), name='movimentacao_detail'),
    ])),
  ]
