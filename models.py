# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2020
# Chenglin Ning, chenglinning@gmain.com
#
import datetime
import uuid

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Numeric
from sqlalchemy import Integer

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class SaledData(Base):
    __tablename__ = "tbl_saled"
    id = Column("id", Integer, primary_key = True, autoincrement=True, nullable=False)
    zone = Column("zone", Text)
    val = Column("val", Numeric(12,2))
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
