# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MouthJournal(models.Model):
    """Journal Model"""

    class Meta(object):
        verbose_name=u'Місячний журнал відвідування'
        verbose_name_plural=u'Місячні журнали відвідування' 


    student = models.ForeignKey('Student',
        verbose_name=u'Студент',
        blank=False,
        unique_for_month='date')

    date = models.DateField(
        verbose_name='Дата',
        blank=False)

    month = locals()
    for num in range(1,32):
        month['present_day'+str(num)]=models.BooleanField(default=False)


    def __str__(self):
        return u"%s: %d, %d" % (self.student.last_name, self.date.mouth, self.date.year)
