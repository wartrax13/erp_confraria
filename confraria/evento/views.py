from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Evento
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
        return redirect(reverse('evento_detail', kwargs={'pk': self.get_object().pk }))