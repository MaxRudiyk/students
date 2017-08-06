# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.views.generic.edit import FormView

from studentsdb.settings import ADMIN_EMAIL

class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):

        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        self.helper.help_text_inline = True         
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.add_input(Submit('send_btn', u'Надіслати'))



    
    from_email = forms.EmailField(label=u'Ваша емейл адреса')
    subject = forms.CharField(label=u'Заголовок листа', max_length=128)
    message = forms.CharField(label=u'Текст повідомлення', max_length=2560, widget=forms.Textarea)


class ContactView(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message'] + ' від ' + from_email

        send_mail(subject, message, from_email, [ADMIN_EMAIL])
        messages.success(self.request, 'Повідомлення успішно надіслане')
        return super(ContactView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ContactView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('contact_admin')







