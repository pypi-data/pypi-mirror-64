# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import django
import pytest
from django.template import Context, Template as T

CTX = Context()


TEMPLATES = (
    ('{% path2css "/test/path/" %}', 'test test-path'),
    ('{% path2css "//" %}', ''),
    ('{% path2css "/test/" prefix="HELLO" %}', 'HELLO-test'),
    ('{% path2css "/test/" prefix="HELLO_" %}', 'HELLO_test'),
    ('{% path2css "/test/" suffix="BYE" %}', 'test-BYE'),
    ('{% path2css "/test/" suffix="_BYE" %}', 'test_BYE'),
    # testing with different separators...
    ('{% path2css "this:is:a_test" split_on=":" %}', 'this this-is this-is-a_test'),
    ('{% path2css "this$£$is$£$a_test" split_on="$£$" %}', 'this this-is this-is-a_test'),
    # Tests with more interesting/exotic/bad request strings (see #2)
    ('{% path2css "/test/…" %}', 'test'),
    ('{% path2css "/test/%E2%80%A6" %}', 'test'),
    ('{% path2css "/test/%E2%80%A6/test2.html" %}', 'test test-test2.html'),
    ('{% path2css "/test/ÅÍÎÏ˝ÓÔÒÚÆ☃" %}', 'test'),
    ('{% path2css "/test/部落格/" %}', 'test'),
    ('{% path2css "/test𝐥𝐚𝐳𝐲" %}', 'test'),
    ('{% path2css "/test/><script>alert(123)</script>" %}', 'test'),
    ('{% path2css \'/test/"><script>alert(123)</script>"<span></span\' %}', 'test test-span'),
    ('{% path2css \'/test/%22%3E%3Cscript%3Ealert%28123%29%3C%2Fscript%3E%22%3Cspan%3E%3C%2Fspan\' %}', 'test'),
)


@pytest.mark.parametrize("template_string,expected_output", TEMPLATES)
def test_templatetag(template_string, expected_output):
    template = r'{% load path2css %}<body class="' + template_string + '">'
    resp = T(template).render(CTX).strip()
    assert resp == '<body class="%s">' % (expected_output,)


@pytest.mark.xfail(condition=django.VERSION[0:2] < (1, 9),
                   reason="Django 1.8 doesn't have combination simple/assignment tags")
@pytest.mark.parametrize("request_path,expected_output", (
    ('/test/', ['test']),
    ("/testa/…", ['testa']),
    ("/testb/%E2%80%A6", ['testb']),
    ("/testc/><script>alert(123)</script>/garble/", ['testc', 'testc-garble']),
    ('/testd/"><script>alert(123)</script>"<span></span', ['testd', 'testd-span']),
    ('/teste/%22%3E%3Cscript%3Ealert%28123%29%3C%2Fscript%3E%22%3Cspan%3E%3C%2Fspan', ['teste']),
))
def test_templatetag_assignment(request_path, expected_output):
    CTX = Context({
        'path': request_path,
    })
    resp = T('''
    {% load path2css %}
    {% path2css path as GOOSE %}
    {% for part in GOOSE %}
    {{part}}
    {% endfor %}
    ''').render(CTX).strip()
    parts = [x.strip() for x in resp.split() if x.strip()]
    assert parts == expected_output
