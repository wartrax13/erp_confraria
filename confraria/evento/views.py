from django.shortcuts import redirect
from django.urls import reverse
from .models import Evento, DoacaoEvento
from confraria.produto.models import Movimentacao, TipoMovimentacaoChoices
from .forms import DoacaoEventoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView


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
    Movimentacao.objects.create(
        tipo=TipoMovimentacaoChoices.SAIDA,
        pessoa_id=pessoa_pk,
        quantidade=1,
        produto_id='produto',
        data='timezone.now',
    )

    categoria = Evento.objects.get(pk=evento_pk) # noqa

    return redirect(reverse('evento_detail', kwargs={'pk': evento_pk}))
