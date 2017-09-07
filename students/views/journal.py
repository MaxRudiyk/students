# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.http import JsonResponse

from ..models import Student, MouthJournal
from ..util import paginate
# Create your views here.

# Views for Students

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        context = super(JournalView, self).get_context_data(**kwargs)

        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()

        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # обчислюємо поточний рік, попередій і наступні місяці
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
    
        context['prev_month'] = prev_month.strftime('%Y-%m-%d') 
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # також поточний місяць
        # змінну cur_month використаємо пізніше в пагінації
        # month_verbose в помісячній навігації
        context['cur_month'] = month.strftime('%Y-%m-%d')

        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d, 'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}for d in range(1, number_of_days+1)]

        # витягуємо усіх студентів відсортований по прізвищу
        queryset = Student.objects.order_by('last_name')

        update_url = reverse('journal')

        students = []

        for student in queryset:
            try:
                journal = MouthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                    })

            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
                })

            context = paginate(students, 3, self.request, context, var_name='students')

        return context

    def post(self, request, *args, **kwargs):

        data = self.request.POST

        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        journal = MouthJournal.objects.get_or_create(student=student, date=month)[0]

        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        return JsonResponse({'key': 'success'})
