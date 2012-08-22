# -*- coding: utf-8 -*-
import json
from datetime import datetime, date
from django.http import HttpResponse
from django.shortcuts import render_to_response
import models
from django.db.models.base import ModelBase

def lst(request):
    """ Render index tables list. """
    context = {}
    context['names'] = []
    for model_name in dir(models):
        if isinstance(getattr(models, model_name), ModelBase):
            model = getattr(models, model_name)
            context['names'].append([model_name, model._struct['title']])

    return render_to_response("lst.html", context)


def table_ajax(request, model_name):
    """ Returns contents if <table_name> in JSON. """
    model = getattr(models, model_name)
    field_names  = [x.name for x in model._meta.fields]
    result = []

    # prepare table headers
    headers = {}
    for field in model._meta.fields:
        headers[field.name] = field.verbose_name
    result.append(headers)

    # prepare data
    for entry in model.objects.all():  
        d={}
        for field_name in field_names:
            value = getattr(entry, field_name)
            if isinstance(value, date): value = value.strftime("%Y %m %d")
            d[field_name] = value
        result.append(d)

    result = json.dumps(result)
    return HttpResponse(result)


def table_struct_ajax(request):
    """ Returns db column types in JSON. """
    result = json.dumps(models.cfg)
    return HttpResponse(result)


def table_update_ajax(request, id):
    """ Performs tables` cell update. """
    try:        
        args = id.split('-')
        model_name = args[0];
        entry_id = args[1];
        field = args[2];

        model = getattr(models, model_name)
        for _field in model._struct['fields']:
            if _field['id'] == field:
                field_type = (_field['type'])

        value = request.POST['value']
        if field_type == 'int':
            value = int(value)
        elif field_type == 'date':
            value = datetime.strptime(value, '%Y %m %d').date()

        entry = model.objects.get(id = int(entry_id))
        setattr(entry, field, value)
        entry.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')
        

def table_add_ajax(request, model_name):
    valid = {}
    model = getattr(models, model_name)
    for field in model._struct['fields']:
        value = request.POST[field['id']]

        field_type = field['type']

        if field_type == 'int':
            value = int(value)
        elif field_type == 'date':
            value = datetime.strptime(value, '%Y %m %d').date()
        valid[field['id']] = value
    entry = model(**valid)
    entry.save()
    valid['id'] = entry.id
    
    # prepare row to output
    for field in valid:
        if isinstance(valid[field], date): valid[field] = valid[field].strftime("%Y %m %d")

    return HttpResponse(json.dumps(valid))








