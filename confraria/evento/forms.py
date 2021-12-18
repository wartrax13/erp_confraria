from django import forms

from django_select2.forms import ModelSelect2Widget

from .models import DoacaoEvento, Evento
from confraria.pessoa.models import Pessoa


class DoacaoEventoForm(forms.ModelForm):

    class Meta:
        model = DoacaoEvento
        fields = ['pessoa']
        widgets = {
            'pessoa': ModelSelect2Widget(
                model=Pessoa,
                search_fields=[
                    'nome__icontains',
                    'cnpj__icontains',
                    'cpf__icontains',
                    'rg__icontains',
                ]
            ),
        }

    def __init__(self, *args, **kwargs):
        self.evento = kwargs.pop('evento', None)
        super().__init__(*args, **kwargs)
        pessoas_adicionadas = Pessoa.objects.filter(doacaoevento__evento=self.evento).values_list('pk', flat=True)
        self.fields['pessoa'].queryset = self.fields['pessoa'].queryset.exclude(pk__in=pessoas_adicionadas)
        self.instance.evento = self.evento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'data', 'categoria']
