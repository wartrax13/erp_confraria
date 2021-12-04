from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PessoaFisicaForm, TelefoneFormSet, PessoaJuridicaForm
from .mixins import FormsetMixin
from .models import PessoaFisica, PessoaJuridica


class PessoaFisicaListView(LoginRequiredMixin, ListView):
    model = PessoaFisica
    paginate_by = 5


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


# PESSOA JURÍDICA


class PessoaJuridicaListView(LoginRequiredMixin, ListView):
    model = PessoaJuridica
    paginate_by = 15


def home(request):
    return render(request, 'base.html')


class PessoaJuridicaUpdateView(LoginRequiredMixin, UpdateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm

    def get_success_url(self):
        return reverse_lazy('pessoajuridica_list')

    def get_form_kwargs(self):
        """Retorna os kwargs que serão passados para instancia do form.
        No caso, o request_user."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


class PessoaJuridicaCreateView(LoginRequiredMixin, CreateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm

    def get_success_url(self):
        return reverse_lazy('pessoajuridica_list')

    def get_form_kwargs(self):
        """Retorna os kwargs que serão passados para instancia do form.
        No caso, o request_user."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['formset'] = self.get_formset()
        return context

    def get_formset(self):
        formset_kwargs = self.get_formset_kwargs()
        return TelefoneFormSet(**formset_kwargs)

    def get_formset_kwargs(self):
        kwargs = {}
        if self.request.method in ['POST', 'PUT']:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update({
                'instance': self.object,
            })

        return kwargs
