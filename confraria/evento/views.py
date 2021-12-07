from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.utils import timezone

from weasyprint import HTML

from .models import Evento, DoacaoEvento
from confraria.produto.models import Movimentacao, TipoMovimentacaoChoices
from .forms import DoacaoEventoForm


class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    paginate_by = 15


class EventoDetail(LoginRequiredMixin, DetailView):
    model = Evento

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form_doacaoevento'] = DoacaoEventoForm()

        return context

    def post(self, request, *args, **kwargs):
        form_doacaoevento = DoacaoEventoForm(data=request.POST, evento=self.get_object())
        if form_doacaoevento.is_valid():
            form_doacaoevento.save()
        else:
            print('abacate')
        return redirect(reverse('evento_detail', kwargs={'pk': self.get_object().pk}))


def receber_doacao(request, evento_pk, pessoa_pk):
    doacao_evento = DoacaoEvento.objects.get(evento_id=evento_pk, pessoa_id=pessoa_pk)
    doacao_evento.recebido = True
    doacao_evento.save()

    categoria = doacao_evento.evento.categoria
    produto = categoria.produto_set.first()

    Movimentacao.objects.create(
        tipo=TipoMovimentacaoChoices.SAIDA,
        pessoa_id=pessoa_pk,
        quantidade=1,
        produto=produto,
        data=timezone.now()
    )

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
