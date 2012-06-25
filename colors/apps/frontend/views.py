# -*- coding: utf-8 -*-

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from colors.apps.api.models import UploadFiles
from colors.apps.api.models import ImageRGB

from colors.common import hex_to_rgb

@csrf_exempt
def index(request):
    params = {}

    ctxt = RequestContext(request, params)
    t = get_template('index.html')
    html = t.render(ctxt)

    return HttpResponse(html)

@csrf_exempt
def test(request):
    params = {}

    ctxt = RequestContext(request, params)
    t = get_template('test.html')
    html = t.render(ctxt)

    return HttpResponse(html)

def view(request, page_id):
    try:
        entry = UploadFiles.objects.get(page_id=page_id, delete_flag=False)
    except:
        raise Http404

    colors_list = entry.colors.split(',')
    colors_dict = {}
    for color in colors_list:
        c = color.split('#')
        colors_dict[c[1]] = color

    params = {
        'page_id': page_id,
        'filename': '%s.jpg' % entry.filename,
        'colors': colors_dict
    }

    ctxt = RequestContext(request, params)
    t = get_template('view.html')
    html = t.render(ctxt)

    return HttpResponse(html)

def find(request, color_id):
    rgb = hex_to_rgb('#%s' % color_id)
    
    try:
        image_list = ImageRGB.objects.select_related()
        image_list = image_list.extra(
            select = {
                'difference': 'POW((%d-red),2) + POW((%d-green),2) + POW((%d-blue),2)' % rgb
            
            },
            order_by = {'difference'}
        )[:1000]
    except:
        raise Http404

    image_result = []
    ignore_id = []
    for image_rgb in image_list:
        if image_rgb.upload_file_id not in ignore_id and image_rgb.difference < 2000:
            image_result.append(UploadFiles.objects.get(pk=image_rgb.upload_file_id))
            ignore_id.append(image_rgb.upload_file_id)

    params = {'image_list': image_result}

    ctxt = RequestContext(request, params)
    t = get_template('list.html')
    html = t.render(ctxt)

    return HttpResponse(html)

