import re
from django.db.models.query_utils import Q
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View, CreateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from confraria.pessoa.views import PessoaFisicaListView, PessoaJuridicaListView

from weasyprint import HTML

from .models import Evento, DoacaoEvento
from confraria.pessoa.models import PessoaFisica, PessoaJuridica, Pessoa
from confraria.produto.models import Movimentacao, TipoMovimentacaoChoices, MovimentacaoProduto
from .forms import DoacaoEventoForm, EventoForm


class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    paginate_by = 15


class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        movimentacao = Movimentacao.objects.create(
            data=form.cleaned_data['data'],
            tipo=TipoMovimentacaoChoices.SAIDA
        )
        form.instance.movimentacao = movimentacao
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('evento_list')


class EventoDetail(LoginRequiredMixin, DetailView):
    model = Evento

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form_doacaoevento'] = DoacaoEventoForm(evento=self.get_object())

        return context

    def filtro_pessoa(self, dados_pessoa):
        pessoa_fisica = PessoaFisica
        pessoa_juridica = PessoaJuridica
        q = Q()
        q = q & Q(nome__icontains=dados_pessoa)
        cpf_rg_cnpj = bool(re.search('.', dados_pessoa))
        
        if cpf_rg_cnpj:
            q = q | (Q(cpf__contains=dados_pessoa) | Q(rg__contains=dados_pessoa) | Q(cnpj__contains=dados_pessoa))

        
        pessoas = pessoa_fisica.objects.filter(q).order_by("nome") or pessoa_juridica.objects.filter(q).order_by("nome")
        return pessoas
    
    def get_queryset(self):
        dados_pessoa = self.request.GET.get('dados_pessoa')
        pessoas = super(EventoDetail, self).get_queryset()
        q = Q()
        
        if dados_pessoa:
            pessoas = pessoas.values()
            pessoa_fisica_juridica = self.filtro_pessoa(dados_pessoa).values()
            pessoa_fisica_juridica.filter(doacaoevento=1)
            q = q & Q(id_pessoa__icontains=dados_pessoa)
        # breakpoint()
        pessoas = pessoas.filter(q).order_by("nome")
        
        return pessoas

    def post(self, request, *args, **kwargs):
        form_doacaoevento = DoacaoEventoForm(data=request.POST, evento=self.get_object())
        if form_doacaoevento.is_valid():
            form_doacaoevento.save()
        # else:
            # messages
        return redirect(reverse('evento_detail', kwargs={'pk': self.get_object().pk}))


@login_required
def receber_doacao(request, evento_pk, pessoa_pk):
    doacao_evento = DoacaoEvento.objects.get(evento_id=evento_pk, pessoa_id=pessoa_pk)

    categoria = doacao_evento.evento.categoria
    produto = categoria.produto_set.first()

    if produto.estoque > 1:
        MovimentacaoProduto.objects.create(
            movimentacao=doacao_evento.evento.movimentacao,
            pessoa_id=pessoa_pk,
            quantidade=1,
            produto=produto
        )

        doacao_evento.recebido = True
        doacao_evento.save()
    else:
        messages.warning(request, 'Sem estoque para realizar a doação')

    return redirect(reverse('evento_detail', kwargs={'pk': evento_pk}))


@login_required
def remover_doacao(request, evento_pk, pessoa_pk):
    doacao_evento = DoacaoEvento.objects.get(evento_id=evento_pk, pessoa_id=pessoa_pk)
    doacao_evento.delete()
    return redirect(reverse('evento_detail', kwargs={'pk': evento_pk}))


@login_required
def cancelar_doacao(request, evento_pk, pessoa_pk):
    doacao_evento = DoacaoEvento.objects.get(evento_id=evento_pk, pessoa_id=pessoa_pk)

    categoria = doacao_evento.evento.categoria
    produto = categoria.produto_set.first()

    movimentacao_produto = MovimentacaoProduto.objects.get(
        movimentacao=doacao_evento.evento.movimentacao,
        pessoa_id=pessoa_pk,
        produto=produto,
    )
    movimentacao_produto.delete()

    doacao_evento.recebido = False
    doacao_evento.save()
    return redirect(reverse('evento_detail', kwargs={'pk': evento_pk}))


class GerarPdfView(View):
    def generate_pdf(self, obj):
        html_string = render_to_string('reports/pdf_template.html', {'obj': obj})
        link = obj.nome
        html = HTML(string=html_string)
        html.write_pdf(target=f'/tmp/{link}.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open(f'{link}.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Transfer-Encoding'] = 'binary'
            response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(link)

            return response

    def get(self, request, *args, **kwargs):
        obj = Evento.objects.get(pk=kwargs['evento_pk'])
        response = self.generate_pdf(obj)
        return response
