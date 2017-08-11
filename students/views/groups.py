# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from ..models import Group, Student
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.

# Views for Groups

def groups_list(request):

    groups = Group.objects.all()

    # Order groups list
    order_by = request.GET.get('order_by', '') # Витягуємо параметр order_by з GET словника
    reverse = request.GET.get('reverse', '') # Витягуємо параметр reverse з GET словника

    if order_by in ('title', 'leader', 'id'):
        groups = groups.order_by(order_by)
        if reverse == '1':
            groups = groups.reverse()

    # Paginate students
    if groups:
        paginator = Paginator(groups, 3)
        page = request.GET.get('page') # Витягуємо параметр page з GET словника
        try: 
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)
    else:  

        groups_list = ''
        
    return render(request, 'students/groups_list.html', {'groups_list': groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Видалення групи відмінено')
            return HttpResponseRedirect(reverse('groups'))
        else:

            if Student.objects.filter(student_group__pk=self.kwargs['pk']):
                messages.error(self.request, "Групу неможливо видалити коли в ній присутній хоча б один студент")
                return HttpResponseRedirect(reverse('groups'))
            else:
                messages.success(self.request, "Групу успішно видалено")
                return super(GroupDeleteView, self).post(request, *args, **kwargs)

def groups_delete(request, gid):

    group = Group.objects.get(pk=gid)

    if request.POST.get('cancel_button'):
        messages.warning(request, 'Видалення групи відмінено')
        return HttpResponseRedirect(reverse('groups'))

    elif request.POST.get('delete_button'):
        
        if Student.objects.filter(student_group__pk=gid):
            messages.error(request, "Групу неможливо видалити коли в ній присутній хоча б один студент")
            return HttpResponseRedirect(reverse('groups'))
        else:
            try:
                group.delete()
                messages.success(request, "Групу успішно видалено")
            except Exception:
                messages.warning(request, 'Виникла непередбачувана помилка')
        return HttpResponseRedirect(reverse('groups'))

    return render(request, 'students/groups_confirm_delete.html', {'group': group})
