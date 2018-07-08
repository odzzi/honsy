# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class MetaModel(models.Model):
    table_name = models.CharField(max_length=256)
    type_name = models.CharField(max_length=256)
    row_id = models.CharField(max_length=256)
    row_value = models.CharField(max_length=256)
    class Meta:
        db_table = 'honsy_meta'