# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import django
import pytest
from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.core.files.base import ContentFile
from django.template import Context, Template as T


CTX = Context()

TEMPLATES = (
    ('{% load path2css %}{% css4path "/test/path/" %}', 'css/test-path.css'),
    ('{% load path2css %}{% css4path "/test/" prefix="HELLO" %}', 'css/HELLO-test.css'),
    ('{% load path2css %}{% css4path "/test/" prefix="HELLO_" %}', 'css/HELLO_test.css'),
    ('{% load path2css %}{% css4path "/test/" suffix="BYE" %}', 'css/test-BYE.css'),
    ('{% load path2css %}{% css4path "/test/" suffix="_BYE" %}', 'css/test_BYE.css'),
    # testing with different separators...
    ('{% load path2css %}{% css4path "test:path" midpoint="__" split_on=":" %}', 'css/test__path.css'),
    # Tests with more interesting/exotic/bad request strings (see #2)
    ('{% load path2css %}{% css4path "/test/…" %}', 'css/test.css'),
    ('{% load path2css %}{% css4path "/test/%E2%80%A6" %}', 'css/test.css'),
    ('{% load path2css %}{% css4path "/test/%E2%80%A6/test2.html" %}', 'css/test-test2.html.css'),
    ('{% load path2css %}{% css4path "/test/ÅÍÎÏ˝ÓÔÒÚÆ☃" %}', 'css/test.css'),
    ('{% load path2css %}{% css4path "/test/部落格/" %}', 'css/test.css'),
    ('{% load path2css %}{% css4path "/test𝐥𝐚𝐳𝐲" %}', 'css/test.css'),
    ('{% load path2css %}{% css4path "/test/><script>alert(123)</script>" %}', 'css/test.css'),
    ('{% load path2css %}{% css4path "/test/-->" %}', 'css/test.css'),
    ('{% load path2css %}{% css4path \'/test/"><script>alert(123)</script>"<span></span\' %}', 'css/test.css'),
    ('{% load path2css %}{% css4path \'/test/%22%3E%3Cscript%3Ealert%28123%29%3C%2Fscript%3E%22%3Cspan%3E%3C%2Fspan\' %}', 'css/test.css'),
)


@pytest.mark.parametrize("template_string,filename", TEMPLATES)
def test_templatetag(template_string, filename):
    storage = StaticFilesStorage(location=settings.STATICFILES_TEST_DIR)
    try:
        storage.save(name=filename, content=ContentFile("body { background: red; }"))
        resp = T(template_string).render(CTX).strip().split("\n")
        expected_output = '<link href="{}{}" rel="stylesheet" type="text/css" />'.format(settings.STATIC_URL, filename)
        assert expected_output in resp
        assert "<!--" not in resp
        assert "-->" not in resp
    finally:
        storage.delete(filename)

def test_templatetag_root_does_nothing():
    resp = T('{% load path2css %}{% css4path "//" %}').render(CTX).strip()
    assert resp == ''


def test_templatetag_multiple_parts_of_path():
    filenames = ('css/level1.css', 'css/level1-level2.css', 'css/level1-level2-level3.css')
    storage = StaticFilesStorage(location=settings.STATICFILES_TEST_DIR)
    try:
        for filename in filenames:
            storage.save(name=filename, content=ContentFile("body { background: red; }"))
        resp = T('{% load path2css %}{% css4path "/level1/level2/level3/" %}').render(CTX).strip()
        assert resp.split("\n") == [
            '<link href="{}css/level1.css" rel="stylesheet" type="text/css" />'.format(settings.STATIC_URL),
            '<link href="{}css/level1-level2.css" rel="stylesheet" type="text/css" />'.format(settings.STATIC_URL),
            '<link href="{}css/level1-level2-level3.css" rel="stylesheet" type="text/css" />'.format(settings.STATIC_URL)
        ]
    finally:
        for filename in filenames:
            storage.delete(filename)


@pytest.mark.xfail(condition=django.VERSION[0:2] < (1, 9),
                   reason="Django 1.8 doesn't have combination simple/assignment tags")
@pytest.mark.parametrize("request_path,filenames", (
    ('/test/path/', ['css/test-path.css']),
    ('/test/path/', ['css/test.css', 'css/test-path.css']),
    ("/test/…", ['css/test.css']),
    ("/test/%E2%80%A6", ['css/test.css']),
    ("/test/%E2%80%A6/test2.html", ['css/test.css', 'css/test-test2.html.css']),
    ("/test/ÅÍÎÏ˝ÓÔÒÚÆ☃", ['css/test.css']),
    ("/test𝐥𝐚𝐳𝐲", ['css/test.css']),
    ("/test/-->/test-other/", ['css/test.css', 'css/test-test-other.css']),
    ("/test/><script>alert(123)</script>", ['css/test.css']),
    ('/test/"><script>alert(123)</script>"<span></span', ['css/test.css', 'css/test-span.css']),
    ("/test/%22%3E%3Cscript%3Ealert%28123%29%3C%2Fscript%3E%22%3Cspan%3E%3C%2Fspan", ['css/test.css']),
))
def test_templatetag_assignment(request_path, filenames):
    storage = StaticFilesStorage(location=settings.STATICFILES_TEST_DIR)
    try:
        for filename in filenames:
            storage.save(name=filename, content=ContentFile("body { background: red; }"))
        resp = T('''
        {% load path2css %}
        {% css4path path as GOOSE %}
        {% for part, exists in GOOSE %}
        {% if exists %}{{ part }}{% endif %}
        {% endfor %}
        ''').render(Context({'path': request_path})).strip()
        parts = [x.strip() for x in resp.split("\n") if x.strip()]
        expected_output = ["{}{}".format(settings.STATIC_URL, filename) for filename in filenames]
        assert parts == expected_output
    finally:
        for filename in filenames:
            storage.delete(filename)
