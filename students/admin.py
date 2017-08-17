# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.core.urlresolvers import reverse
from copy import deepcopy
from django.forms import ModelForm, ValidationError

from .models import Student, Group, Exam, Result_exam
from django.http import Http404


# Register your models here.

class StudentFormAdmin(ModelForm):

    class Meta():
        model = Student
        fields = '__all__'

    def clean_student_group(self):
        """Check if student is leader in any group.
        If yes, then ensure it`s the same as selected group."""

        group = Group.objects.filter(leader=self.instance)
        if self.cleaned_data['student_group'] != group[0]:
                raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')
        
        return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
    actions = ['copy_student']
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket','notes']
    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

    def copy_student(self, request, queryset):

        old_obj = deepcopy(queryset)
        flag = False
        count = 0

        for s in old_obj:
            try:
                s.pk = None
                count = count + 1 
                flag = True
                s.save() 
            except Exception:
                flag = False

        if flag:
            if count == 1:
                self.message_user(request, 'Successfully copy %s Student' % (count))
            else:
                self.message_user(request, 'Successfully copy %s Students' % (count))
        else:
            self.message_user(request, 'Copy is falied')


class GroupFormAdmin(ModelForm):

    class Meta():
        model = Group
        fields = '__all__'

    def clean_leader(self):
        """Check if student is in the group."""
        students = Student.objects.filter(student_group=self.instance)
        flag = False
        if self.cleaned_data['leader'] is None:
            return self.cleaned_data['leader']
        
        if not students.exists():
            raise ValidationError(u'Група порожня', code='invalid')

        for student in students:

            if self.cleaned_data['leader'] == student:
                return self.cleaned_data['leader']
            else: 
                flag = True

        if flag:
            raise ValidationError(u'Студент не навчається в даній групі', code='invalid')


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    ordering = ['title']
    list_per_page = 10
    search_fields = ['title', 'leader__last_name', 'leader__first_name']
    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'gid': obj.id})

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Result_exam)
