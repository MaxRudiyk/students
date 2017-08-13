# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import Student, Group, Exam, Result_exam


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable=['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket','notes']

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
admin.site.register(Exam)
admin.site.register(Result_exam)
