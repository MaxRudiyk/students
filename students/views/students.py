# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.template.loader import render_to_string

from ..models import Student, Group

# Create your views here.

# Views for Students

def students_list(request):

    students = Student.objects.all()

    # Order students list
    order_by = request.GET.get('order_by', '') # Витягуємо параметр order_by з GET словника
    reverse = request.GET.get('reverse', '') # Витягуємо параметр reverse з GET словника

    if order_by in ('last_name', 'first_name', 'ticket', 'id'):
        students = students.order_by(order_by)
        if reverse == '1':
            students = students.reverse()

    # Paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page') # Витягуємо параметр page з GET словника
    try: 
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):

    groups_list = Group.objects.all().order_by('title')

    if request.method == 'POST':

        if request.POST.get('add_button') is not None:
            
            errors = {}

            if not errors:
                student = Student(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    middle_name=request.POST['middle_name'],
                    birthday=request.POST['birthday'],
                    ticket=request.POST['ticket'],
                    student_group=groups_list.get(pk=request.POST['student_group']),
                    photo=request.FILES['photo'],)

                student.save()

                return HttpResponseRedirect(reverse('home'))

            else:

                return render(request, 'students/students_add.html', {'groups_list': groups_list, 'errors': errors})

        elif request.POST.get('cancel_button') is not None:

            return HttpResponseRedirect(reverse('home'))

    else: 

        return render(request, 'students/students_add.html', {'groups_list': groups_list})

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
