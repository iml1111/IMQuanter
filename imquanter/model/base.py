from abc import ABCMeta, abstractmethod
from MySQLdb.connections import Connection


class BaseModel(metaclass=ABCMeta):
    """Model Interface"""
    TABLE_QUERY = None

    def __init__(self, db: Connection):
        self._db = db
        self.table = self.__class__.__name__
        if self.TABLE_QUERY is None:
            raise NotImplementedError('TABLE QUERY가 입력되야 함.')
        self._create_table()

    def select_all(self):
        query = f'SELECT * FROM {self.table}'
        with self._db.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return results

    def _create_table(self):
        with self._db.cursor() as cursor:
            cursor.execute(self.TABLE_QUERY % self.table)