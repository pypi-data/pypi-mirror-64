# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.conf.urls import url
from django.http import HttpResponse
from django.template import Context
from django.template import Template


def view(request, arg1, arg2, kws):
    template = Template("""<!DOCTYPE html>
    <html><head></head>
    <body>
    <pre>arg1={{ arg1 }}, arg2={{ arg2 }}, using kwargs={{ kws }}</pre>
    <hr>
    {% load path2css %}
    <pre>{% path2css request.path %}</pre>
    </body>
    </html>""")
    context = {
        'arg1': arg1,
        'arg2': arg2,
        'kws': kws,
        'request': request
    }
    return HttpResponse(template.render(Context(context)))

urlpatterns = [
    url(r'^test/(.+)/pos/(.+)/yay/$', view, name='testview_pos', kwargs={'kws': False}),
    url(r'^test/(?P<arg1>.+)/kw/(?P<arg2>.+)/yay/$', view, name='testview_kw', kwargs={'kws': True}),
]

