# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def show_main(request):
    return render(request,'main.html')




# Create your views here.
