from config import settings
from database import MSSQLDatabase


def init_db_instance():
    return MSSQLDatabase()


def load_exchanges():
    query = settings.EXCHANGES_DB_QUERY
    conn = init_db_instance()
    df = conn.select_table(query)
    data = [tuple(row.values()) for row in df.to_dict("records")]
    return data


def load_tickers():
    query = settings.TICKERS_DB_QUERY
    conn = init_db_instance()
    df = conn.select_table(query)
    data = [tuple(row.values()) for row in df.to_dict("records")]
    return data
