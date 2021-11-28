from django.shortcuts import render
from .models import Produto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    paginate_by = 15
