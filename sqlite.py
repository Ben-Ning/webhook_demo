# -*- coding: utf-8 -*-
# Copyright (C) 2016-2020 
# Chenglin Ning, chenglinning@gmain.com
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool
from sqlalchemy.pool import QueuePool
from sqlalchemy.pool import NullPool

from singleton import singleton_sqlite
from models import Base
import traceback

@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
    except:
        raise exc.DisconnectionError()

@singleton_sqlite
class SQLite():
    def __init__(self, dbname="master.db"):
        self.dbname = dbname
        self.dbengine = None
        self.dbsession_class = None
 
    def createEngine(self):
        db_string = "sqlite:///./%s" % ( self.dbname )
        if self.dbengine == None:
            self.dbengine = create_engine(db_string, poolclass=NullPool)
        if self.dbengine:
            logging.info("SQLite connect: %s OK" % (db_string))
        else:
            logging.info("SQLite connect: %s Failure" % (db_string))
        return self.dbengine

    def getSessionClass(self):
        assert(self.dbengine)
        return sessionmaker(bind=self.dbengine)
        
def getMDBSessionClass(dbname='master.db'):
    db = SQLite(dbname=dbname)
    db.createEngine()
    return db.getSessionClass()

def getMDatabaseInstance(dbname='master.db'):
    db = SQLite(dbname=dbname)
    db.createEngine()
    return db

def getMDatabaseEngine(dbname='master.db'):
    db = SQLite(dbname=dbname)
    db.createEngine()
    return db.dbengine
