# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Views for Students

def students_list(request):
	students = (
		{'id': 1, 'first_name': u'Максим', 'last_name': u'Рудюк', 'ticket': 2587, 'image': 'img/max.jpg'},
		{'id': 2, 'first_name': u'Ананстасія', 'last_name': u'Перевалова', 'ticket': 2874, 'image': 'img/default-user.png'},
		{'id': 3, 'first_name': u'Віталій', 'last_name': u'Нікітчин', 'ticket': 2174, 'image': 'img/default-user.png'},)
	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)

# Views for Groups

def groups_list(request):
	return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)