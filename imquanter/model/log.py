"""
실행 기록 테이블
"""
from typing import Optional
from .base import BaseModel


class Log(BaseModel):
    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `action` VARCHAR(20) NOT NULL,
        `payload` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`action`, `payload`)
    )
    """

    def log_action(
            self,
            action: str,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        query = f"""
        REPLACE INTO {self.table} (
            action, payload
        )
        VALUES (%s, %s)
        """
        payload = self.collect_payload(symbol, start_date, end_date)
        with self._db.cursor() as cursor:
            cursor.execute(query, (action, payload))

    def already_exists(
            self,
            action: str,
            symbol: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None):
        payload = self.collect_payload(symbol, start_date, end_date)
        query = f"""
        SELECT * FROM {self.table}
        WHERE `action` = %s and `payload` = %s
        """
        with self._db.cursor() as cursor:
            cursor.execute(query, (action, payload))
            result = cursor.fetchone()
        return bool(result)

    @staticmethod
    def collect_payload(symbol: str, start_date: str, end_date: str):
        return f"{symbol}_{start_date}_{end_date}"