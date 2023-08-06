#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..protocols import http

NB = "http://d-nb.info"
NB_SCHEMA = ["lds", "marcxml", "bibframe"]


def address(idn, schema):
    """
    """
    return "{0}/{1}/about/{2}".format(NB, idn, schema)


def request(idn, schema="lds"):
    """
    """
    url = address(idn, schema)
    return http.get_request(url)
