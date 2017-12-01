# -*- coding: utf-8 -*-
# Copyright (C) 2016-2020.
# Chenglin Ning, chenglinning@gmain.com
# 
# Source code free for education and evlalution.
# If commercial and bussiness purpose or redistribution 
# as free or non-free software please contact the author.
# Other rights not metioned before are all reserved.

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    
    return _singleton

def singleton_sqlite(cls):
    sqlite_instances = {}
    def _singleton(*args, **kwargs):
        if 'dbname' in kwargs:
            mydbname = kwargs['dbname']
        else:
            mydbname = 'master.db'

        if mydbname not in sqlite_instances:
            sqlite_instances[mydbname] = cls(*args, **kwargs)
        return sqlite_instances[mydbname]
    
    return _singleton

