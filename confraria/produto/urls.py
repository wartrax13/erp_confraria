from django.urls import path, include
from .views import (
  ProdutoListView, ProdutoCreateView, ProdutoUpdateView,
  MovimentacaoListView, MovimentacaoCreateView, MovimentacaoDetailView,
  CategoriaCreateView, CategoriaListView, GerarPdfMovimentacaoView
  )

urlpatterns = [
    path('list/', ProdutoListView.as_view(), name='produto_list'),
    path('create/', ProdutoCreateView.as_view(), name='produto_form'),
    path('update/<int:pk>/', ProdutoUpdateView.as_view(), name='produto_form'),
    path('categoria/', CategoriaCreateView.as_view(), name='categoria_form'),
    path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
    path('movimentacao/', include([
        path('list/', MovimentacaoListView.as_view(), name='movimentacao_list'),
        path('create/', MovimentacaoCreateView.as_view(), name='movimentacao_form'),
        path('detail/<int:pk>/', MovimentacaoDetailView.as_view(), name='movimentacao_detail'),
        path('pdf_movimentacao/<int:pk>/', GerarPdfMovimentacaoView.as_view(), name='movimentacao_pdf')
    ])),
  ]
