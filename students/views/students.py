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
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from ..forms import StudentUpdateForm, StudentAddForm

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


class StudentAddView(CreateView):
    template_name = 'students/students_form.html'
    form_class = StudentAddForm
    model = Student

    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(request, 'Додавання студента відмінено')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.success(request, 'Студента успішно збережено')
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Видалення студента відмінено')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.success(self.request, "Студента успішно видалено")
            return super(StudentDeleteView, self).post(request, *args, **kwargs)


class StudentUpdateView(UpdateView):
    template_name = 'students/students_form.html'
    form_class = StudentUpdateForm
    model = Student

    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(request, 'Редагування студента відмінено')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.success(request, 'Студента успішно збережено')
            return super(StudentUpdateView, self).post(request, *args, **kwargs)
