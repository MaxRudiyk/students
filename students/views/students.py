# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from ..models import Student, Group
from datetime import datetime

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

    if request.method == 'POST': # Was form posted

        if request.POST.get('add_button') is not None: # Was form add btn cliked
            
            errors = {} # errors collection

            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}

            # validate user input 
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name 

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коретний формат дати"
                data['ticket'] = ticket    

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Ім'я є обов'язковим"
            else:
                groups = groups_list.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo


            if not errors:
                # Create student object
                student = Student(**data)
                student.save() # save to db
                messages.success(request, 'Студента %s успішно додано' % student)
                return HttpResponseRedirect(reverse('home'))

            else:
                messages.warning(request, 'Виправте наступні помилки')
                return render(request, 'students/students_add.html', {'groups_list': groups_list, 'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, 'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))

    else: 

        return render(request, 'students/students_add.html', {'groups_list': groups_list})

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
