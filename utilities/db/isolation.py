from enum import Enum

from django.db import connection


class IsolationLevel(Enum):
    SERIALIZABLE = 'SERIALIZABLE'


def set_isolation_level(level: IsolationLevel):
    cursor = connection.cursor()
    cursor.execute('SET TRANSACTION ISOLATION LEVEL {}'.format(level.value))
