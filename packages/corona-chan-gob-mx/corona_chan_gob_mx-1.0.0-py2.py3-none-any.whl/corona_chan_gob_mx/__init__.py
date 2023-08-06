# -*- coding: utf-8 -*-
from functools import reduce

from corona_chan_gob_mx.scraper import list_of_pdf


def get_today_cases():
    links = list_of_pdf.get()
    tables = map( lambda link: link.get().native, links.native )
    result = reduce( lambda x, y: x + y, tables )
    return result


__author__ = """dem4ply"""
__email__ = 'dem4ply@gmail.com'
__version__ = '1.0.0'
