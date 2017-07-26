# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Student, Group, Exam, Result_exam


# Register your models here.

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Exam)
admin.site.register(Result_exam)
