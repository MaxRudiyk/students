# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


from datetime import datetime

from ..models import Student, Group
from ..forms import StudentUpdateForm, StudentAddForm
from ..util import paginate

# Create your views here.

# Views for Students
class StudentList(TemplateView):
    template_name = 'students/students_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)

        students = Student.objects.all()

        # Order students list
        order_by = self.request.GET.get('order_by', '') # Витягуємо параметр order_by з GET словника
        reverse = self.request.GET.get('reverse', '') # Витягуємо параметр reverse з GET словника

        if order_by in ('last_name', 'first_name', 'ticket', 'id'):
            students = students.order_by(order_by)
            if reverse == '1':
                students = students.reverse()

        context = paginate(students, 3, self.request, context, var_name='students')

        return context

class StudentAddView(CreateView):
    template_name = 'students/universal_form.html'
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
    template_name = 'students/confirm_delete.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        context = super(StudentDeleteView, self).get_context_data(**kwargs)
        context['question'] = u'Ви дійсно бажаєте видалити студента'
        context['title'] = u'Видалити студента'
        context['context_url'] = 'students_delete'
        context['context_id'] = self.kwargs['pk']
        return context

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
    template_name = 'students/universal_form.html'
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


def student_delete(request, sid):

    student = Student.objects.get(pk=sid)

    if request.POST.get('cancel_button'):
        messages.warning(request, 'Видалення студента скасовано')
        return HttpResponseRedirect(reverse('home'))

    elif request.POST.get('delete_button'):
        
        try:
            student.delete()
            messages.success(request, 'Студента успішно видалено')
        except Exception:
            messages.warning(request, 'Виникла непередбачувана помилка')

        return HttpResponseRedirect(reverse('home'))

    return render(request, 'students/students_confirm_delete.html', {'student': student})