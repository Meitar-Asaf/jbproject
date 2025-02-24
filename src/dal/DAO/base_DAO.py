from src import config
import psycopg2 as pg


class BaseDAO:
    def __init__(self, connection_details: str):
        self.connection_details = connection_details
