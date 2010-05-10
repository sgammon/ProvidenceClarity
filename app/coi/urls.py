# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule


def get_rules():
    """Returns a list of URL rules for the Hello, World! application."""

    rules = [
        Rule('/', endpoint='hello-world', handler='coi.handlers.HelloWorldHandler'),
        Rule('/pretty', endpoint='hello-world-pretty', handler='coi.handlers.PrettyHelloWorldHandler'),
    ]

    return rules
