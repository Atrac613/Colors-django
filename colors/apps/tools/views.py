# -*- coding: utf-8 -*-

import uuid
import datetime
import simplejson
import colorsys

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from colors.apps.api.models import ColorNameJa
from colors.apps.api.models import ColorNameEn

from colors.common import hex_to_rgb

from colors.settings import BASE_DIR

def insertColorNameJa(request):
    filename = '%s/tools/scrape/color_names_ja.json' % BASE_DIR

    f = open(filename)
    contents = f.read()
    json = simplejson.loads(contents)

    for row in json:
        name = row['kanji']
        name_yomi = row['yomi']
        rgb = hex_to_rgb(row['hex'])
        
        try:
            color_name = ColorNameJa.objects.get(name=name, red=rgb[0], green=rgb[1], blue=rgb[2])
        except:
            color_name = ColorNameJa()
            color_name.name = name
            color_name.name_yomi = name_yomi
            color_name.red = rgb[0]
            color_name.green = rgb[1]
            color_name.blue = rgb[2]
            color_name.save()

    return HttpResponse('done.')

def insertColorNameEn(request):
    filename = '%s/tools/scrape/color_names_en.json' % BASE_DIR

    f = open(filename)
    contents = f.read()
    json = simplejson.loads(contents)

    for row in json:
        name = row['name']

        try:
            rgb = hex_to_rgb(row['hex'])

            try:
                color_name = ColorNameEn.objects.get(name=name, red=rgb[0], green=rgb[1], blue=rgb[2])
            except:
                color_name = ColorNameEn()
                color_name.name = name
                color_name.red = rgb[0]
                color_name.green = rgb[1]
                color_name.blue = rgb[2]
                color_name.save()
        except:
            pass

    return HttpResponse('done.')

