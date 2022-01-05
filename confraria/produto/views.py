from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.urls import reverse_lazy

from confraria.mixins import FormsetMixin
from .forms import ProdutoForm, MovimentacaoForm, CategoriaForm, MovimentacaoFormSet
from .models import Produto, Movimentacao, Categoria

# pdf

from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from weasyprint import HTML


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    paginate_by = 15

    def get_queryset(self):
        nome_produto = self.request.GET.get('nome')
        produto_disponivel = self.request.GET.get('disponibilidade')
        produtos = super(ProdutoListView, self).get_queryset()
        q = Q()
        objects_id = (obj.id for obj in produtos if obj.disponibilidade is True)

        if nome_produto:
            q = q & Q(nome__icontains=nome_produto)

        if produto_disponivel:
            q = q & Q(id__in=objects_id)

        produtos = produtos.filter(q).order_by("nome")

        return produtos


class ProdutoCreateView(LoginRequiredMixin, CreateView):
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
    ordering = ['-data']


class MovimentacaoCreateView(LoginRequiredMixin, FormsetMixin, CreateView):
    model = Movimentacao
    form_class = MovimentacaoForm
    formset_class = MovimentacaoFormSet

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        form = self.get_form()
        kwargs['form_kwargs'] = {
            'tipo': form['tipo'].value()
        }
        return kwargs

    def get_success_url(self):
        return reverse_lazy('movimentacao_list')


class MovimentacaoDetailView(LoginRequiredMixin, DetailView):
    model = Movimentacao


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm

    def get_success_url(self):
        return reverse_lazy('categoria_list')


class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria


class GerarPdfMovimentacaoView(View):
    def generate_pdf(self, obj):
        html_string = render_to_string('reports/pdf_template_movimentacao.html', {'obj': obj})
        link = obj.numero_oficio
        html = HTML(string=html_string, base_url=self.request.build_absolute_uri())
        html.write_pdf(target=f'/tmp/{link}.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open(f'{link}.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Transfer-Encoding'] = 'binary'
            response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(link)

            return response

    def get(self, request, *args, **kwargs):
        obj = Movimentacao.objects.get(pk=kwargs['pk'])
        response = self.generate_pdf(obj)
        return response
