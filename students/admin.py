# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import Student, Group, Exam, Result_exam
from copy import deepcopy


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    actions = ['copy_student']
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable=['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket','notes']

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

    def copy_student(self, request, queryset):
        old_obj = deepcopy(queryset)
        for s in old_obj:
            try:
                s.pk = None
                s.save()
                self.message_user(request, 'Successfully copy students')
            except Exception:
                self.message_user(request, 'Copy is falied')

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_per_page = 10
    search_fields = ['title', 'leader__last_name', 'leader__first_name']

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Result_exam)
