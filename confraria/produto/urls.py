from django.urls import path
from .views import ProdutoListView, ProdutoCreateView, ProdutoUpdateView

urlpatterns = [
    path('list/', ProdutoListView.as_view(), name='produto_list'),
    path('create/', ProdutoCreateView.as_view(), name='produto_form'),
    path('update/<int:pk>/', ProdutoUpdateView.as_view(), name='produto_form'),
  ]
