# -*- encoding=utf-8 -*-
# Author:QiQi
from datetime import datetime
import sys
import uuid
import sqlalchemy
import binascii
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, String, Integer, DateTime, func, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# reload(sys)
# sys.setdefaultencoding('gbk')

Base = declarative_base()


class IfJobMod(Base):
    __tablename__ = "If_job"
    IfJobId = Column("If_job_id", String(36), primary_key=True)
    pjId = Column("Pj_id", BigInteger)
    storeId = Column("Store_id", BigInteger, default=0)
    createTime = Column("Create_time", DateTime, default=func.getdate())
    operateTime = Column("Operate_time", DateTime, default=func.getdate())
    idIndex = Column("Id_index", Integer, autoincrement=True, primary_key=True)
    refIfId = Column("Ref_if_id", String, default="")  # ref_if_id
    status = Column("Status", Integer, default=0)
    ifLineIndex = Column("If_line_index", Integer, default=0)
