# -*- coding: utf-8 -*-
from django.db import models
import yaml, json
from django.db.models.base import ModelBase
from django.db.models.fields import Field


def read_cfg(path):
    data = open(path, 'r').read()
    cfg = yaml.load(data)
    return cfg

MODEL_CONFIG_PATH = 'testapp/models.cfg'

cfg = read_cfg(MODEL_CONFIG_PATH)

def construct_fields(cfg, model_name):
    class Meta:
        verbose_name = cfg[model_name]['title']
        verbose_name_plural = verbose_name

    fields = {}
    for field in cfg[model_name]['fields']:
        if field['type'] == 'char':
            fields[field['id']] = models.CharField(field['title'], max_length=field['max_length'])
        elif field['type'] == 'int':
            fields[field['id']] = models.IntegerField(field['title'])
        elif field['type'] == 'date':
            fields[field['id']] = models.DateField(field['title'])
        else:
            raise Exception('Incorrect field type in yaml file %s .' % field['type'])

    fields['__module__']    = 'testapp.models'
    fields['Meta']          = Meta
    fields['_struct']       = cfg[model_name]

    return fields
    
for model_name in cfg:
    vars()[model_name] = type(model_name, (models.Model,), construct_fields(cfg, model_name))

