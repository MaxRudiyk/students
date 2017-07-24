# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from ..models import Group

# Create your views here.

# Views for Groups

def groups_list(request):

    groups = Group.objects.all()

    # Order groups list
    order_by = request.GET.get('order_by', '')
    reverse = request.GET.get('reverse', '')

    if order_by in ('title', 'leader', 'id'):
        groups = groups.order_by(order_by)
        if reverse == '1':
            groups = groups.reverse()

    # Paginate students
    if groups:
        paginator = Paginator(groups, 3)
        page = request.GET.get('page')
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

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)