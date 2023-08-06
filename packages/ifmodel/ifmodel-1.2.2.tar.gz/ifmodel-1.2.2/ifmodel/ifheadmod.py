# -*- encoding=utf-8 -*-
# Author:QiQi
from datetime import datetime
import sys
import uuid
import sqlalchemy
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, String, Integer, DateTime, func, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# reload(sys)
# sys.setdefaultencoding('gbk')
Base = declarative_base()


class IfHeadMod(Base):
    __tablename__ = "If_head"
    IfHeadId = Column("If_head_id", String(36), primary_key=True)
    pjId = Column("Pj_id", BigInteger)
    ifJobId = Column("If_job_id", String(36))
    storeId = Column("Store_id", BigInteger, default=0)
    origFrom = Column("Orig_from", String, default="")
    fileName = Column("File_name", String)
    fileType = Column("File_type", String)
    sheetName = Column("Sheet_name", String, default="")
    dir = Column("Dir", String)
    operateUserId = Column("Operate_user_id", Integer)
    createTime = Column("Create_time", DateTime, default=func.getdate())
    status = Column("Status", Integer, default=0)
    reason = Column("Reason", String, default="")
    remark = Column("Remark", String, default="")
    idIndex = Column("Id_index", Integer, autoincrement=True, primary_key=True)
    dateBegin = Column("Date_begin", DateTime)
    dateEnd = Column("Date_end", DateTime)
    IfLineIndex = Column("If_id_index", String)
    OriginFileName = Column("Origin_file_name", String)
