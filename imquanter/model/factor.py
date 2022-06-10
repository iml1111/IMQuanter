"""
가치 지표 수집 테이블
"""
from .base import BaseModel


class Factor(BaseModel):

    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `symbol` VARCHAR(20) NOT NULL,
        `year` VARCHAR(10) NOT NULL,
        `quarter` VARCHAR (10) NOT NULL,
        `eps` DOUBLE NOT NULL,
        `per` DOUBLE NOT NULL,
        `bps` DOUBLE NOT NULL,
        `pbr` DOUBLE NOT NULL,
        `roe` DOUBLE NOT NULL,
        `roa` DOUBLE NOT NULL,
        PRIMARY KEY (`symbol`, `year`, `quarter`)
    )
    """