# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from ..models import Student

# Create your views here.

# Views for Students

def students_list(request):
    students = Student.objects.all()

    # Order students list
    order_by = request.GET.get('order_by', '')
    reverse = request.GET.get('reverse', '')

    if order_by in ('last_name', 'first_name', 'ticket', 'id'):
        students = students.order_by(order_by)
        if reverse == '1':
            students = students.reverse()


    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
