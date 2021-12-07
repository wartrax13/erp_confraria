from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PessoaFisicaForm, TelefoneFormSet, PessoaJuridicaForm, TelefonePessoaJuridicaFormSet
from .mixins import FormsetMixin
from .models import PessoaFisica, PessoaJuridica


class PessoaFisicaListView(LoginRequiredMixin, ListView):
    model = PessoaFisica
    paginate_by = 5

    def get_queryset(self):
        nome_pessoa = self.request.GET.get('nome')
        pessoas = PessoaFisica.objects.all()

        if nome_pessoa:
            pessoas = PessoaFisica.objects.filter(nome__icontains=nome_pessoa)

        return pessoas


class PessoaFisicaUpdateView(LoginRequiredMixin, FormsetMixin, UpdateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    formset_class = TelefoneFormSet

    def get_success_url(self):
        return reverse_lazy('pessoafisica_list')

    def get_form_kwargs(self):
        """Retorna os kwargs que serão passados para instancia do form.
        No caso, o request_user."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class PessoaFisicaCreateView(LoginRequiredMixin, FormsetMixin, CreateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    formset_class = TelefoneFormSet

    def get_success_url(self):
        return reverse_lazy('pessoafisica_list')

    def get_form_kwargs(self):
        """Retorna os kwargs que serão passados para instancia do form.
        No caso, o request_user."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class PessoaFisicaDetailView(LoginRequiredMixin, DetailView):
    model = PessoaFisica


# PESSOA JURÍDICA


class PessoaJuridicaListView(LoginRequiredMixin, ListView):
    model = PessoaJuridica
    paginate_by = 15

    def get_queryset(self):
        nome_pessoa = self.request.GET.get('nome')
        pessoas = PessoaJuridica.objects.all()

        if nome_pessoa:
            pessoas = PessoaJuridica.objects.filter(nome__icontains=nome_pessoa)

        return pessoas


def home(request):
    return render(request, 'base.html')


class PessoaJuridicaUpdateView(LoginRequiredMixin, FormsetMixin, UpdateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    formset_class = TelefonePessoaJuridicaFormSet

    def get_success_url(self):
        return reverse_lazy('pessoajuridica_list')

    def get_form_kwargs(self):
        """Retorna os kwargs que serão passados para instancia do form.
        No caso, o request_user."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class PessoaJuridicaCreateView(LoginRequiredMixin, FormsetMixin, CreateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    formset_class = TelefonePessoaJuridicaFormSet

    def get_success_url(self):
        return reverse_lazy('pessoajuridica_list')

    def get_form_kwargs(self):
        """Retorna os kwargs que serão passados para instancia do form.
        No caso, o request_user."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class PessoaJuridicaDetailView(LoginRequiredMixin, DetailView):
    model = PessoaJuridica
