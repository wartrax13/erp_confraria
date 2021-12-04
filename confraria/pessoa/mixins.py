from django.db import transaction
from django.http import HttpResponseRedirect


class FormsetMixin:
    def get_formset_class(self):
        return self.formset_class

    def get_formset(self):
        formset_kwargs = self.get_formset_kwargs()
        FormsetClass = self.get_formset_class()
        return FormsetClass(**formset_kwargs)

    def get_context_data(self, *args, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = self.get_formset()
        return super().get_context_data(*args, **kwargs)

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

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def form_valid(self, form, formset):
        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except AttributeError:
            self.object = None
        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)
