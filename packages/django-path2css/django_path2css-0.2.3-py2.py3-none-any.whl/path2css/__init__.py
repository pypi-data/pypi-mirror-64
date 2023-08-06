# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import warnings
from itertools import chain

try:
    from django.urls import Resolver404, resolve
except ImportError:
    from django.core.urlresolvers import Resolver404, resolve
from django.utils.encoding import force_text
from django.utils.html import escape, format_html

import codecs
try:
    from collections import UserList
except ImportError:
    from UserList import UserList
from django.utils.six import python_2_unicode_compatible, string_types
from django.utils.six.moves.urllib import parse

__version_info__ = '0.2.3'
__version__ = '0.2.3'
version = '0.2.3'
VERSION = '0.2.3'
__all__ = ['get_version', 'generate_css_names_from_string',
           'request_path_to_css_names']

def get_version():
    return version  # pragma: no cover


def _generate_css_names_from_string(item, split_on, prefix='', suffix='', midpoint=''):
    split_path = item.strip(split_on).split(split_on)
    # Refs #2 - If there's anything urlencoded, decode it.
    unquoted_path = (parse.unquote(item).strip() for item in split_path)
    # Refs #2 - Make sure we only bother with ought-to-be-safe ascii
    # rather than full unicode planes.
    decoded_path = (codecs.decode(part.encode('utf-8'), "ascii", "ignore") for part in unquoted_path)
    # Refs #2 - Don't take anything which needed escaping (ie: included < or & etc)
    escaped_path = (item for item in decoded_path if escape(item) == item)
    newpath = tuple(part for part in escaped_path if part)
    # If the thing is empty, just return an empty tuple
    if not newpath:
        return ()
    newpath_length = len(newpath) + 1
    variations = (newpath[0:l] for l in range(1, newpath_length))
    # If there's a prefix and it doesn't end with a sensible separator (given
    # the valid names of CSS identifiers), add midpoint.
    if prefix and not prefix.endswith(('-', '_')):
        prefix = '%s%s' % (prefix, midpoint)
    # same as prefix, but start, rather than end
    if suffix and not suffix.startswith(('-', '_')):
        suffix = '%s%s' % (midpoint, suffix,)
    finalised_variations = (
        '%s%s%s' % (prefix, midpoint.join(variation), suffix)
        for variation in variations
    )
    return finalised_variations


def generate_css_names_from_string(item, split_on, prefix='', suffix='', midpoint=''):
    seen = set()
    complete_variations = _generate_css_names_from_string(
        item=item, split_on=split_on, prefix=prefix, suffix=suffix,
        midpoint=midpoint)
    for variation in complete_variations:
        if variation not in seen:
            seen.add(variation)
            yield variation
    # Given a URL which includes, say, 2 dynamic parts like so:
    # /section/<DYNAMIC>/comments/<DYNAMIC>/details/
    # try and get the following variations:
    # section section-comments section-comments-details
    static_variations = ()
    try:
        matched_view = resolve(item)
    except Resolver404:
        pass
    else:
        dynamic_parts = chain(matched_view.args, matched_view.kwargs.values())
        dynamic_strs = (x for x in dynamic_parts
                        if isinstance(x, string_types))
        item_copy = item
        for to_replace in dynamic_strs:
            item_copy = item_copy.replace(to_replace, '', 1)
        static_variations = _generate_css_names_from_string(
            item_copy, split_on=split_on, prefix=prefix,
            suffix=suffix, midpoint=midpoint)
    for extra_variation in static_variations:
        if extra_variation not in seen:
            seen.add(extra_variation)
            yield extra_variation



def request_path_to_css_names(item, prefix='', suffix='', midpoint=''):
    # TODO: remove this function.
    warnings.warn(
        "request_path_to_css_names() is scheduled to be removed, and should be "
        "replaced with generate_css_names_from_string() with a valid "
        "split_on argument",
        PendingDeprecationWarning
    )
    return generate_css_names_from_string(item=item, split_on='/',
                                          prefix=prefix, suffix=suffix,
                                          midpoint=midpoint)


@python_2_unicode_compatible
class Output(UserList):
    string_template = "{}"
    string_separator = " "

    def rendered(self):
        for x in self.data:
            yield format_html(self.string_template, force_text(x))

    def __str__(self):
        """
        Used when doing something like:
        {% path2css ... as OUTVAR %}
        {{ OUTVAR }}
        """
        parts = self.rendered()
        return self.string_separator.join(parts)

    def __html__(self):
        """
        Used in {% path2css x y %} is used directly
        """
        return force_text(self)

    """
    __getitem__ is used when doing something like:
    {% path2css ... as OUTVAR %}
    {% for x in OUTVAR %}{{ x }}{% endfor %}
    """


class LinkOutput(Output):
    string_template = '<link href="{}" rel="stylesheet" type="text/css" />'
    string_separator = "\n"

    def rendered(self):
        for x, found in self.data:
            data = format_html(self.string_template, force_text(x))
            if found:
                yield data
            else:
                yield "<!-- {} -->".format(data)

    """
    __getitem__ is used when doing something like:
    {% path2css ... as OUTVAR %}
    {% for x, did_file_exist in OUTVAR %}{{ x }}={{ did_file_exist }}{% endfor %}
    """


def context_processor(request):
    return {
        "PATH2CSS": Output(generate_css_names_from_string(request.path, split_on='/',midpoint='-')),
    }
