# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name=u'Іспит'
        verbose_name_plural=u'Іспити' 

    subject = models.CharField(
        max_length=256, 
        blank=False, 
        verbose_name=u"Назва предмету")

    teacher_name = models.CharField(
        max_length=256, 
        blank=False, 
        verbose_name=u"ПІБ викладача")

    exams_group = models.ForeignKey('Group',
        verbose_name=u'Група',
        blank=False)

    date_of_exam = models.DateTimeField(
        blank=False, 
        verbose_name=u'Дата і час проведення')

    notes = models.TextField(
        blank=True,
        verbose_name=u'Додаткові нотатки',
        null=True)

    def __str__(self):
        return u"%s (%s)" % (self.subject, self.teacher_name)
