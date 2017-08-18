# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Exam





class ExamUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(ExamUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('exams_edit', kwargs={'pk': kwargs['instance'].id})

        self.helper.help_text_inline = True         
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-default"),
        )

class ExamAddForm(forms.ModelForm):
    
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(ExamAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('exams_add')

        self.helper.help_text_inline = True         
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-default"),
        )


