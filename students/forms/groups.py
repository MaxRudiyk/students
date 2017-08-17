# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Group, Student

class GroupUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})

        self.helper.help_text_inline = True         
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-default"),
        )

    def clean_leader(self):
        """Check if student is in the group."""
        students = Student.objects.filter(student_group=self.instance)
        flag = False
        if self.cleaned_data['leader'] is None:
            return self.cleaned_data['leader']
        
        if not students.exists():
            raise forms.ValidationError(u'Група порожня', code='invalid')

        for student in students:

            if self.cleaned_data['leader'] == student:
                return self.cleaned_data['leader']
            else: 
                flag = True

        if flag:
            raise forms.ValidationError(u'Студент не навчається в даній групі', code='invalid')

class GroupAddForm(forms.ModelForm):
    
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(GroupAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('groups_add')

        self.helper.help_text_inline = True         
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-default"),
        )


