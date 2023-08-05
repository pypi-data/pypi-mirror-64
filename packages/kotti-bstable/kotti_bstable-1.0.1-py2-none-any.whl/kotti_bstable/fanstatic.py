# -*- coding: utf-8 -*-

"""
Created on 2020-03-21
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from __future__ import absolute_import, division, print_function

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource


library = Library("kotti_bstable", "static")

bootstrap_table = Group([
    Resource(library, "ext/bootstrap-table/dist/bootstrap-table.min.css"),
    Resource(
        library,
        "ext/bootstrap-table/dist/bootstrap-table.min.js")
])

bootstrap_table_date_picker = Group([
    Resource(library, "ext/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css"),
    Resource(
        library,
        "ext/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js",
        depends=[bootstrap_table]
    )
])

bootstrap_table_filter_control = Group([
    Resource(library, "ext/bootstrap-table/dist/extensions/filter-control/bootstrap-table-filter-control.css"),
    Resource(
        library,
        "ext/bootstrap-table/dist/extensions/filter-control/bootstrap-table-filter-control.min.js",
        depends=[bootstrap_table, bootstrap_table_date_picker]
    )
])

select2_component = Group([
    Resource(library, "ext/select2/dist/css/select2.min.css"),
    Resource(library, "ext/select2/dist/js/select2.min.js")
])

font_awesome = Resource(library, "ext/font-awesome/css/font-awesome.min.css")

css_and_js = Group([bootstrap_table, bootstrap_table_filter_control])
