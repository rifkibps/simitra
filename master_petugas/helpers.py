# -*- coding: utf-8 -*-
# CREDITS: https://github.com/django-import-export/django-import-export/issues/152#issuecomment-68824452
from __future__ import unicode_literals

import datetime
from django.utils.six import moves
import xlrd
import tablib
from import_export import instance_loaders, resources, widgets
from import_export.formats.base_formats import TablibFormat
from xlrd import xldate_as_tuple


class ExcelDataset(tablib.Dataset):
    """
    A tablib Dataset that knows the Excel datemode
    """
    excel_datemode = None


class XLS(TablibFormat):
    """
    Use standalone xlrd to create DataSet from modern Excel files, avoiding
    old vendored versions of xlrd and openpyxl in tablib
    @TODO review when https://github.com/kennethreitz/tablib/issues/167 is resolved to just leave the datemode
    """
    TABLIB_MODULE = 'tablib.formats._xls'

    def can_import(self):
        return True

    def is_binary(self):
        """
        Returns if this format is binary.
        """
        return True

    def create_dataset(self, in_stream):
        """
        Create dataset from first sheet.
        """
        xls_book = xlrd.open_workbook(file_contents=in_stream)
        dataset = ExcelDataset()
        dataset.excel_datemode = xls_book.datemode
        sheet = xls_book.sheets()[0]

        dataset.headers = sheet.row_values(0)
        for i in moves.range(1, sheet.nrows):
            dataset.append(sheet.row_values(i))
        return dataset


class ExcelDateWidget(widgets.Widget):
    """
    Widget for converting date fields.
    Takes optional ``format`` parameter.
    Treats float dates as Excel using the supplied datemode, defaulting to Windows
    """
    def __init__(self, dateformat=None, datemode=0):
        if dateformat is None:
            dateformat = "%Y-%m-%d"
        self.dateformat = dateformat
        self.datemode = datemode

    def clean(self, value, row=None, *args, **kwargs):
        import logging

        logger = logging.getLogger(__name__)

        if not value:
            return None
        try:
            return datetime.date(*xldate_as_tuple(value, self.datemode)[0:3])
        except ValueError:
            try:
                return datetime.datetime.strptime(value, self.dateformat).date()
            except TypeError:
                logger.debug("Cannot create Date object from " + str(value))

    def render(self, value, obj=None):
        return value.strftime(self.dateformat)