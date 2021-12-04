from django import forms
from .models import DoacaoEvento  # Evento


class DoacaoEventoForm(forms.ModelForm):

    class Meta:
        model = DoacaoEvento
        fields = ['pessoa']

    def __init__(self, *args, **kwargs):
        self.evento = kwargs.pop('evento', None)
        super().__init__(*args, **kwargs)
        self.instance.evento = self.evento
