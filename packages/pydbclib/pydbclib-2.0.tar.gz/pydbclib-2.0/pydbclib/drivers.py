# -*- coding: utf-8 -*-
"""
@time: 2020/3/18 2:36 下午
@desc:
"""
import sys
from abc import ABC, abstractmethod

from log4py import Logger

from pydbclib.sql import default_place_holders, compilers


class Driver(ABC):

    def __init__(self, *args, **kwargs):
        self.driver = kwargs.pop('driver', "sqlalchemy")
        self._session = None
        self.connection = self.connect(*args, **kwargs)

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def session(self):
        pass

    def execute(self, sql, params=None, **kw):
        pass

    def execute_many(self, sql, params=None, **kw):
        pass

    def fetchone(self):
        return self.session.fetchone()

    def fetchmany(self, batch_size):
        return self.session.fetchmany(batch_size)

    def fetchall(self):
        return self.session.fetchall()

    def rowcount(self):
        return self.session.rowcount

    def description(self):
        return self.session.description

    def rollback(self):
        self.connection.rollback()

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.session is not None:
            self.session.close()
        if self.connection is not None:
            self.connection.close()


@Logger.class_logger()
class CommonDriver(Driver):

    def __init__(self, *args, **kwargs):
        self._dbapi = None
        place_holder = kwargs.pop("place_holder", "default")
        super().__init__(*args, **kwargs)
        dbapi_name, *_ = self._dbapi.split(".", 1)
        self.place_holder = default_place_holders.get(dbapi_name) or place_holder
        self.compiler = compilers[self.place_holder]

    def connect(self, *args, **kwargs):
        if hasattr(self.driver, "cursor"):
            self._dbapi = self.driver.__module__
            return self.driver
        else:
            __import__(self.driver)
            self._dbapi = self.driver
            driver = sys.modules[self.driver]
            return driver.connect(*args, **kwargs)

    @property
    def session(self):
        if not self._session:
            self._session = self.connection.cursor()
        return self._session

    def execute(self, sql, params=None, **kw):
        sql, params = self.compiler(sql, params).process_one()
        params = params if params else []
        self.logger.info("{}, {}".format(sql, params))
        self.session.execute(sql, params, **kw)

    def execute_many(self, sql, params=None, **kw):
        sql, params = self.compiler(sql, params).process()
        params = params if params else []
        self.logger.info("{}, {}".format(sql, params))
        self.session.executemany(sql, params, **kw)


@Logger.class_logger()
class SQLAlchemyDriver(Driver):

    def __init__(self, *args, **kwargs):
        self._cursor = None
        super().__init__(*args, **kwargs)

    def connect(self, *args, **kwargs):
        from sqlalchemy import engine
        if isinstance(self.driver, engine.base.Engine):
            return self.driver
        else:
            from sqlalchemy import create_engine
            return create_engine(*args, **kwargs)

    @property
    def session(self):
        if not self._session:
            from sqlalchemy.orm import sessionmaker
            self._session = sessionmaker(bind=self.connection)()
        return self._session

    def execute(self, sql, params=None, **kw):
        self.logger.info("{}, {}".format(sql, params))
        self._cursor = self.session.execute(sql, params, **kw)

    def execute_many(self, sql, params=None, **kw):
        self.logger.info("{}, {}".format(sql, params))
        self._cursor = self.session.execute(sql, params, **kw)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchmany(self, batch_size):
        return self._cursor.fetchmany(batch_size)

    def fetchall(self):
        return self._cursor.fetchall()

    def rowcount(self):
        return self._cursor.rowcount

    def description(self):
        return self._cursor._cursor_description()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def close(self):
        if self.session is not None:
            self.session.close()
