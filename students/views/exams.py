# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from ..models import Exam, Result_exam

# Create your views here.

# Views for Exams

def exams_list(request):
    exams = Exam.objects.all()
    return render(request, 'students/exams_list.html', {'exams_list': exams})

def exams_result(request, param1, param2): # Param1 - Назва Групи Param2 - назва предмету
	results_list = Result_exam.objects.filter(students__student_group__title='%s' % param1).filter(subject__subject='%s' % param2)
	results_list.order_by('students')
	return render(request, 'students/results_list.html', {'results_list': results_list})
   	#return HttpResponse('<h1>Result for %s %s</h1>' % (param1, param2))

def exams_add(request):
    return HttpResponse('<h1>Exam Add Form</h1>')

def exams_edit(request, eid):
    return HttpResponse('<h1>Edit Exam %s</h1>' % eid)

def exams_delete(request, eid):
    return HttpResponse('<h1>Delete Exam %s</h1>' % eid)
