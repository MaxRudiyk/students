# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models import Exam, Result_exam
from ..forms import ExamAddForm, ExamUpdateForm


# Create your views here.

# Views for Exams

def exams_list(request):
    exams = Exam.objects.all()

    # Paginate students
    paginator = Paginator(exams, 3)
    page = request.GET.get('page') # Витягуємо параметр page з GET словника
    try: 
        exams = paginator.page(page)
    except PageNotAnInteger:
        exaams = paginator.page(1)
    except EmptyPage:
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exams_list.html', {'exams_list': exams})

def exams_result(request, param1, param2): # Param1 - Назва Групи Param2 - назва предмету
    results_list = Result_exam.objects.filter(students__student_group__title='%s' % param1).filter(subject__subject='%s' % param2)
    results_list.order_by('students')
    return render(request, 'students/results_list.html', {'results_list': results_list})
    #return HttpResponse('<h1>Result for %s %s</h1>' % (param1, param2))

class ExamAddView(CreateView):
    template_name = 'students/universal_form.html'
    form_class = ExamAddForm
    model = Exam

    def get_success_url(self):
        return reverse('exams')

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(request, 'Додавання іспиту відмінено')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.success(request, 'Іспит успішно збережено')
            return super(ExamAddView, self).post(request, *args, **kwargs)


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/confirm_delete.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        context = super(ExamDeleteView, self).get_context_data(**kwargs)
        context['question'] = u'Ви дійсно бажаєте видалити іспит'
        context['title'] = u'Видалити іспит'
        context['context_url'] = 'exams_delete'
        context['context_id'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Видалення іспиту відмінено')
            return HttpResponseRedirect(reverse('exams'))
        else:
            messages.success(self.request, "Іспит успішно видалено")
            return super(ExamDeleteView, self).post(request, *args, **kwargs)


class ExamUpdateView(UpdateView):
    template_name = 'students/universal_form.html'
    form_class = ExamUpdateForm
    model = Exam

    def get_success_url(self):
        return reverse('exams')

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(request, 'Редагування іспиту відмінено')
            return HttpResponseRedirect(reverse('exams'))
        else:
            messages.success(request, 'Іспит успішно збережено')
            return super(ExamUpdateView, self).post(request, *args, **kwargs)
