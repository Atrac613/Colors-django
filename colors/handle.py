# -*- coding: utf-8 -*-

def handle_uploaded_file(f, filename):
    destination = open(filename, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)


