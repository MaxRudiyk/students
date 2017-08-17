# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Group, Student


class StudentUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})

        self.helper.help_text_inline = True         
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-default"),
        )

    def clean_student_group(self):
        """Check if student is leader in any group.
        If yes, then ensure it`s the same as selected group."""

        group = Group.objects.filter(leader=self.instance)
        if self.cleaned_data['student_group'] != group[0]:
                raise forms.ValidationError(u'Студент є старостою іншої групи.', code='invalid')
        
        return self.cleaned_data['student_group']

class StudentAddForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(StudentAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('students_add')

        self.helper.help_text_inline = True         
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout[7] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-default"),
        )


