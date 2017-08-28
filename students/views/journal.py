# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models import Student, MouthJournal
from ..util import paginate
# Create your views here.

# Views for Students

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        context = super(JournalView, self).get_context_data(**kwargs)

        if self.request.GET.get('month'):
            month = datetime.strftime(self.request.GET['month'], '%Y-%m-%d').date()

        else:
            today = datatime.today()
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
        context['cur_month'] = '2017-08-01'
        context['month_verbose'] = u'Серпень'

        # тут буде обчислюватись список днів у місяці,
        # а поки напишемо статично
        context['month_header'] = [
            {'day':1, 'verbose': Пн},
            {'day':2, 'verbose': Вт},
            {'day':3, 'verbose': Ср},
            {'day':4, 'verbose': Чт},
            {'day':5, 'verbose': Пт}]

        # витягуємо усіх студентів відсортований по прізвищу
        queryset = Student.objects.order_by('last_name')

        update_url = reverse('journal')

        students = []

        for student in queryset:
            # TODO: витягуємо журнал для студента і вибраного місяця
            # набиваємо дні для студента
            days = []
            for day in range(1, 31):
                days.append({
                    'day': day,
                    'present': True,
                    'date': date(2017, 8, day).strftime('%Y-%m-%d'),})

            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,})

            context = paginate(students, 10, self.request, context, var_name='students')

            return context 