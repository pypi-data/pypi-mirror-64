#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..protocols import http

GND = "http://d-nb.info/gnd"
GND_SCHEMA = ["lds", "marcxml"]


def address(idn, schema):
    return "{0}/{1}/about/{2}".format(GND, idn, schema)


def request(idn, schema="lds"):
    url = address(idn, schema)
    return http.get_request(url)
