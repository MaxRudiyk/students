# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Result_exam(models.Model):
    """Result Exam Model"""

    class Meta(object):
        verbose_name=u'Результат'
        verbose_name_plural=u'Результати' 

    subject = models.ForeignKey('Exam', 
        blank=False, 
        verbose_name=u"Предмет")

    students = models.ForeignKey('Student',
        blank=False,
        null=True,
        verbose_name=u"Студент")

    # Hunderd Point Scale - hps (По 100 бальній шкалі)
    hps = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Оцінка",
        null=True )

    def __str__(self):
        return u"%s (%s)" % (self.students, self.students.student_group)
