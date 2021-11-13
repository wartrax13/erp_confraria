from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import PessoaFisica, PessoaJuridica
from .forms import PessoaFisicaForm

class PessoaFisicaListView(ListView):
    model = PessoaFisica
    paginate_by = 15


class PessoaFisicaCreateView(CreateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm

    def get_success_url(self):
        return reverse_lazy('pessoafisica_list')

    def get_form_kwargs(self):
        """Retorna os kwargs que serão passados para instancia do form.
        No caso, o request_user."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class PessoaJuridicaListView(ListView):
    model = PessoaJuridica
    paginate_by = 15


def home(request):
    return render(request, 'base.html')
