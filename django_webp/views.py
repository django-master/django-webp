# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('django_webp/index.html')