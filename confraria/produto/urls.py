from django.urls import path
from django.urls.conf import include
from .views import ProdutoListView, ProdutoCreateView

urlpatterns = [
    path('list/', ProdutoListView.as_view(), name='produto_list'),
    path('create/', ProdutoCreateView.as_view(), name='produto_form'),
  ]
