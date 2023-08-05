#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import inspect
from sqlalchemy.orm.interfaces import (ONETOMANY, MANYTOMANY)
from sqlalchemy.types import DateTime, Integer
from flask_sqlalchemy import Pagination


class Column(object):
    def __init__(self, model):
        self.inp = inspect(model)
        self.columns = self.inp.columns

    @property
    def primary_columns(self):
        return [column for column in self.columns if column.primary_key]

    @property
    def nullable_columns(self):
        return [column for column in self.columns if column.nullable]

    @property
    def notnullable_columns(self):
        return [
            column for column in self.columns
            if not column.nullable and not column.primary_key
        ]

    @property
    def unique_columns(self):
        return [column for column in self.columns if column.unique]

    @property
    def relation_columns(self):
        return [relation for relation in self.inp.relationships]

    @property
    def datetime_columns(self):
        return [
            column for column in self.columns
            if isinstance(column.type, DateTime)
        ]

    @property
    def integer_columns(self):
        return [
            column for column in self.columns
            if isinstance(column.type, Integer)
        ]

    @property
    def foreign_keys(self):
        columns = []
        [columns.extend(list(column.foreign_keys)) for column in self.columns]
        return [i.parent for i in columns]


class PageInfo(object):
    '''
    just for flask_sqlalchemy
    '''

    def __init__(self, paginate):
        self.paginate = paginate

    def as_dict(self):
        pageinfo = {
            'items': True,
            'pages': self.paginate.pages,
            'has_prev': self.paginate.has_prev,
            'page': self.paginate.page,
            'has_next': self.paginate.has_next,
            'iter_pages': list(
                self.paginate.iter_pages(
                    left_edge=1, left_current=2, right_current=3,
                    right_edge=1))
        }
        return pageinfo


class Field(object):
    def __init__(self, source, args={}, default=None):
        self.source = source
        self.args = args
        self.default = default

    def data(self, instance):
        if hasattr(instance, self.source):
            source = getattr(instance, self.source)
            if not callable(source):
                return source
            return source(**self.args)
        return self.default

import json
import  datetime
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

class Serializer(object):
    def __init__(self, instance, **kwargs):
        meta = self.Meta
        self.instance = instance
        self.depth = kwargs['depth'] if 'depth' in kwargs else meta.depth
        self.include = kwargs[
            'include'] if 'include' in kwargs else meta.include
        self.exclude = kwargs[
            'exclude'] if 'exclude' in kwargs else meta.exclude
        self.extra = kwargs['extra'] if 'extra' in kwargs else meta.extra

    def __new__(self, *args, **kwargs):
        meta = self.Meta
        for _meta in ['include', 'exclude', 'extra']:
            if not hasattr(meta, _meta):
                setattr(meta, _meta, [])
        if not hasattr(meta, 'depth'):
            setattr(meta, 'depth', 2)
        return object.__new__(self)

    @property
    def data(self):
        if isinstance(self.instance, Pagination):
            self.instance = self.instance.items
        if isinstance(self.instance, list):
            return  json.loads(json.dumps(self._serializerlist(self.instance, self.depth),cls=DateEncoder))
        return json.loads(json.dumps(self._serializer(self.instance, self.depth),cls=DateEncoder))

    def _serializerlist(self, instances, depth):
        results = []
        for instance in instances:
            result = self._serializer(instance, depth)
            if result:
                results.append(result)
        return results

    def _serializer(self, instance, depth):
        result = {}
        if depth == 0:
            return result
        depth -= 1
        model_class = self.get_model_class(instance)
        inp = self.get_inspect(model_class)
        model_data = self._serializer_model(inp, instance, depth)
        relation_data = self._serializer_relation(inp, instance, depth)
        extra_data = self._serializer_extra(instance)
        result.update(model_data)
        result.update(relation_data)
        result.update(extra_data)
        return result

    def _serializer_extra(self, instance):
        extra = self.extra
        result = {}
        for e in extra:
            # extra_column = getattr(self, e)
            # if isinstance(extra_column, Field):
            #     result[e] = extra_column.data(instance)
            # else:
            extra_column = getattr(instance, e)
            result[e] = extra_column if not callable(
                extra_column) else extra_column()
        return result

    def _serializer_model(self, inp, instance, depth):
        result = {}
        model_columns = self.get_model_columns(inp)
        for column in model_columns:

            result[column] = getattr(instance, column)
        return result

    def _serializer_relation(self, inp, instance, depth):
        result = {}
        relation_columns = self.get_relation_columns(inp)
        for relation in relation_columns:
            column = relation.key
            serializer = Serializer
            if hasattr(self, column):
                serializer = getattr(self, column)
            if relation.direction in [ONETOMANY, MANYTOMANY
                                      ] and relation.uselist:
                children = getattr(instance, column)
                if relation.lazy == 'dynamic':
                    children = children.all()
                result[column] = serializer(
                    children, exclude=[relation.back_populates,"delivery_date"],
                    depth=depth).data if children else []
            else:
                child = getattr(instance, column)
                if relation.lazy == 'dynamic':
                    child = child.first()
                result[column] = serializer(
                    child, exclude=[relation.back_populates],
                    depth=depth).data if child else {}
        return result

    def get_model_class(self, instance):
        return getattr(instance, '__class__')

    def get_inspect(self, model_class):
        return inspect(model_class)

    def get_model_columns(self, inp):
        if self.include:
            model_columns = [
                column.name for column in inp.columns
                if column.name in self.include
            ]
            print("0-0--")
            model_columns = []
            for column in inp.columns:
                import datetime
                print(column.type)
                if isinstance(column.type, datetime.datetime):
                    print("-========")
                    print(column)
                    column = str(datetime)
                    model_columns.append(column.name)
        elif self.exclude:
            # self.exclude=self.exclude.append("delivery_date")
            if self.exclude:
                self.exclude.append("delivery_date")
            else:
                self.exclude=["delivery_date"]
            model_columns = [
                column.name for column in inp.columns
                if column.name not in self.exclude
            ]
        else:
            model_columns = [column.name for column in inp.columns]

        return model_columns

    def get_relation_columns(self, inp):
        if self.include:
            relation_columns = [
                relation for relation in inp.relationships
                if relation.key in self.include
            ]
        elif self.exclude:
            relation_columns = [
                relation for relation in inp.relationships
                if relation.key not in self.exclude
            ]
        else:
            relation_columns = [relation for relation in inp.relationships]
        return relation_columns

    class Meta:
        depth = 2
        include = []
        exclude = []
        extra = []
