from django.shortcuts import render
from django.views.generic import ListView
from .models import PessoaFisica


class PessoaFisicaListView(ListView):
    model = PessoaFisica
    paginate_by = 20


def home(request):
    return render(request, 'base.html')
