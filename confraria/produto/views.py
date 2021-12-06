from .models import Produto, Movimentacao
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import ProdutoForm, MovimentacaoForm
from django.urls import reverse_lazy


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    paginate_by = 15


class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm

    def get_success_url(self):
        return reverse_lazy('produto_list')


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm

    def get_success_url(self):
        return reverse_lazy('produto_list')


class MovimentacaoListView(LoginRequiredMixin, ListView):
    model = Movimentacao
    paginate_by = 15


class MovimentacaoCreateView(CreateView):
    model = Movimentacao
    form_class = MovimentacaoForm

    def get_success_url(self):
        return reverse_lazy('movimentacao_list')


class MovimentacaoDetailView(LoginRequiredMixin, DetailView):
    model = Movimentacao
