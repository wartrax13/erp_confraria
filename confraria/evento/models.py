from django.db import models
# from confraria.produto.models import Categoria

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
# from django_object_actions import DjangoObjectActions


class Evento(models.Model):
    nome = models.CharField('Nome', max_length=128)
    data = models.DateField('Data')
    # categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.nome

    def generate_pdf(self, request, obj):
        html_string = render_to_string('reports/pdf_template.html', {'obj': obj})

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/{}.pdf'.format(obj))

        fs = FileSystemStorage('/tmp')
        with fs.open('{}.pdf'.format(obj)) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(obj)
            return response

        return response

    generate_pdf.label = 'Gerar PDF'
    generate_pdf.short_description = 'Clique para gerar o PDF dessa ordem de serviço'

    change_actions = ('generate_pdf',)


class DoacaoEvento(models.Model):
    pessoa = models.ForeignKey('pessoa.Pessoa', on_delete=models.PROTECT)
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    recebido = models.BooleanField(default=False)
    data_entrega = models.DateTimeField('Data de entrega', null=True, blank=True)

    class Meta:
        verbose_name = 'Doação de Evento'
        verbose_name_plural = 'Doações de Eventos'
        unique_together = ['pessoa', 'evento']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.evento.nome}'
