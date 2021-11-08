from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import PessoaFisica, PessoaJuridica
from .forms import PessoaFisicaForm

class PessoaFisicaListView(ListView):
    model = PessoaFisica
    paginate_by = 15


class PessoaFisicaCreateView(CreateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm


class PessoaJuridicaListView(ListView):
    model = PessoaJuridica
    paginate_by = 15




def home(request):
    return render(request, 'base.html')
