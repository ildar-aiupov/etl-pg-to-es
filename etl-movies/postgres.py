import logging

import psycopg2.extras
import psycopg2

from backoff import backoff
from state import State
import sql_queries


class Postgres:
    PORTION_SIZE = 100

    def __init__(self, params):
        self.params = params
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    @backoff()
    def get_connection(self):
        return psycopg2.connect(**self.params)

    def check_updates(self, state):
        last_update = state.get_last_update()
        self.cursor.execute(sql_queries.select_ids, (last_update,))
        self.filmwork_ids = self.cursor.fetchall()
        if self.filmwork_ids:
            self.filmwork_ids = tuple(element["id"] for element in self.filmwork_ids)
        return len(self.filmwork_ids)

    def load_portion(self):
        self.cursor.execute(sql_queries.select_data, [self.filmwork_ids])
        while portion := self.cursor.fetchmany(self.PORTION_SIZE):
            logging.info(f"Loaded next portion of {len(portion)} entries")
            yield portion
