# -*- coding:utf-8 -*-
""" Some interesting data structures not provided by Python."""

__author__ = "Wang Hewen"

import collections

class DefaultOrderedDict(collections.OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, collections.Callable)):
            raise TypeError('first argument must be callable')
        collections.OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return collections.OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, list(self.items())

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(list(self.items())))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               collections.OrderedDict.__repr__(self))

class NestedDict(dict):
    '''
    Implementation of perl's autovivification feature(i.e. Nested dicts). 
    E.g. 

    a = NestedDict()

    a[1][2][3] = 4
    a[1][3][3] = 5
    a[1][2]['test'] = 6

    print a
    '''
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value