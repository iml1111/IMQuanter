from .base import BaseModel



class Factor(BaseModel):

    TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS %s (
        `symbol` VARCHAR(20) NOT NULL,
        `year` VARCHAR(10) NOT NULL,
        `quarter` VARCHAR (10) NOT NULL,
        `assets` BIGINT NOT NULL,
        `equity` BIGINT NOT NULL,
        `liability` BIGINT NOT NULL,
        `profit` BIGINT NOT NULL,
        `total_stocks` BIGINT,
        PRIMARY KEY (`symbol`, `year`, `quarter`)
    )
    """