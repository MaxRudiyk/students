# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Group(models.Model):
    
    """ Groups model"""

    class Meta(object):
        verbose_name=u'Група'
        verbose_name_plural=u'Групи'
        ordering = ['title']

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u'Назва')

    leader = models.OneToOneField('Student',
        verbose_name=u'Староста',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name=u'Додаткові нотатки')


    def __str__(self):
        #if self.leader:
            #return u"%s (%s %s)" % (self.title, self.leader.first_name, self.leader.last_name)
        #else:
        return u"%s" % (self.title)

            
        

