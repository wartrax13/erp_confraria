from .models import Produto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .forms import ProdutoForm
from django.urls import reverse_lazy


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    paginate_by = 15


class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm

    def get_success_url(self):
        return reverse_lazy('produto_list')

    # continuar
