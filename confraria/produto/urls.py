from django.urls import path
from .views import ProdutoListView

urlpatterns = [
    path('list/', ProdutoListView.as_view(), name='produto_list'),
]
