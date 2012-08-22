# -*- coding: utf-8 -*-
from django.contrib import admin
import models
from django.db.models.base import ModelBase

for mdl in dir(models):
    if isinstance(getattr(models, mdl), ModelBase):
         admin.site.register(getattr(models, mdl))

