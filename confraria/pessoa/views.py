import re
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import PessoaFisicaForm, TelefoneFormSet, PessoaJuridicaForm, TelefonePessoaJuridicaFormSet
from confraria.mixins import FormsetMixin
from .models import PessoaFisica, PessoaJuridica
from confraria.produto.models import Movimentacao, MovimentacaoProduto


class PessoaFisicaListView(LoginRequiredMixin, ListView):
    model = PessoaFisica
    paginate_by = 15

    def get_queryset(self):
        dados_pessoa = self.request.GET.get('dados_pessoa')
        pessoas = super(PessoaFisicaListView, self).get_queryset()
        q = Q()

        if dados_pessoa:
            q = q & Q(nome__icontains=dados_pessoa)
            cpf_rg = bool(re.search('.', dados_pessoa))
            if cpf_rg:
                q = q | (Q(cpf__contains=dados_pessoa) | Q(rg__contains=dados_pessoa))

        pessoas = pessoas.filter(q).order_by("nome")
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
        dados_empresa = self.request.GET.get('dados_empresa')
        empresas = super(PessoaJuridicaListView, self).get_queryset()
        q = Q()

        if dados_empresa:
            q = q & Q(nome__icontains=dados_empresa)
            cnpj = bool(re.search('.', dados_empresa))
            if cnpj:
                q = q | Q(cnpj__contains=dados_empresa)

        empresas = empresas.filter(q).order_by("nome")
        return empresas


class Intro(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Intro, self).get_context_data(*args, **kwargs)
        context['movimentacoes'] = Movimentacao.objects.all().count()
        context['movimentacaoproduto'] = MovimentacaoProduto.objects.all().count()
        context['saida'] = Movimentacao.objects.filter(tipo='saida').count()
        context['entrada'] = Movimentacao.objects.filter(tipo='entrada').count()
        context['total_pessoas'] = PessoaFisica.objects.all().count()
        context['total_instituicoes'] = PessoaJuridica.objects.all().count()
        return context


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
