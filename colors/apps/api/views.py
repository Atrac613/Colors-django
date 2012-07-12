# -*- coding: utf-8 -*-

import uuid
import datetime
import simplejson
import colorsys

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from colors.apps.api.models import UploadFiles
from colors.apps.api.models import ImageRGB
from colors.apps.api.models import ImageHSV
from colors.apps.api.models import ColorNameJa
from colors.apps.api.models import ColorNameEn
from colors.apps.api.forms import UploadFilesForm

from colors.common import gen_imagekey
from colors.common import gen_thumbnail
from colors.common import get_colors
from colors.common import get_colors_recursive
from colors.common import rgb_to_hex
from colors.common import hex_to_rgb
from colors.handle import handle_uploaded_file

from colors.settings import BASE_DIR
from colors.settings import STATICFILES_DIRS
from colors.settings import MEDIA_ROOT

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid() is not True:
            raise Exception('Invalid file data.')

        redirect = request.POST.get('redirect', 'false')

        filehash = '%s' % str(uuid.uuid4())

        if request.FILES['file'].content_type == 'image/png':
            filename = '%s.png' % filehash
        else:
            filename = '%s.jpg' % filehash

        dest_filename = '%s/images/%s' % (MEDIA_ROOT, filename)

        handle_uploaded_file(request.FILES['file'], dest_filename)

        thumb_filename = '%s/thumb_%s.jpg' % (STATICFILES_DIRS[0][1], filehash)
        gen_thumbnail(dest_filename, thumb_filename)

        file_ = ContentFile(open(thumb_filename, 'r').read())
        default_storage.save('%s.jpg' % filehash, file_)

        page_id = gen_imagekey(length=8)

        upload_file = UploadFiles(filename=filehash, page_id=page_id, colors='', created_at=datetime.datetime.now())
        upload_file.save()

        colors_list = get_colors_recursive(dest_filename, 4)
        colors_hex_list = []
        
        for row in colors_list:
            rgb = (row[0], row[1], row[2])
            colors_hex_list.append(rgb_to_hex(rgb))

            image_rgb = ImageRGB(upload_file=upload_file, red=rgb[0], green=rgb[1], blue=rgb[2])
            image_rgb.save()

            hsv = colorsys.rgb_to_hsv(rgb[0] / 255., rgb[1] / 255., rgb[2] / 255.)
            image_hsv = ImageHSV(upload_file=upload_file, hue=hsv[0] * 360, saturation=hsv[1] * 100, value=hsv[2] * 100)
            image_hsv.save()

        colors = ','.join(colors_hex_list)

        upload_file.colors = colors
        upload_file.save()

        if redirect == 'true':
            return HttpResponseRedirect('/p/%s' % page_id)
        else:
            return HttpResponse(simplejson.dumps({'filename': filename, 'page_id': page_id}))

    else:
        raise Http404

def findColorName(request, color_id):
    try:
        rgb = hex_to_rgb('#%s' % color_id)
    except:
        raise Http404

    name_list_ja = None
    try:
        name_list_ja = ColorNameJa.objects.select_related()
        name_list_ja = name_list_ja.extra(
            select = {
                'difference': 'POW((%d-red),2) + POW((%d-green),2) + POW((%d-blue),2)' % rgb

            },
            order_by = {'difference'}
        )[:1000]
    except:
        pass

    name_list_en = None
    try:
        name_list_en = ColorNameEn.objects.select_related()
        name_list_en = name_list_en.extra(
            select = {
                'difference': 'POW((%d-red),2) + POW((%d-green),2) + POW((%d-blue),2)' % rgb

            },
            order_by = {'difference'}
        )[:1000]
    except:
        pass

    name_result = []

    for row in name_list_ja:
        if row.difference < 2000:
            name_result.append({
                'name': '%s(%s)' % (row.name, row.name_yomi),
                'hex': rgb_to_hex((row.red, row.green, row.blue)),
                'lang': 'ja_JP'
            })

    for row in name_list_en:
        if row.difference < 2000:
            name_result.append({
                'name': row.name,
                'hex': rgb_to_hex((row.red, row.green, row.blue)),
                'lang': 'en_US'
            })

    return HttpResponse(simplejson.dumps(name_result))

