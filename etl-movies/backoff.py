from functools import wraps
from time import sleep
from pip._vendor import requests
import logging

import psycopg2


def backoff(start_sleep_time=0.01, factor=2, border_sleep_time=10, is_connection=True):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            _factor = factor
            counter = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except psycopg2.OperationalError:
                    logging.info("Postgres connection error. Trying to reconnect...")
                except requests.exceptions.ConnectionError:
                    logging.info(
                        "Elasticsearch connection error. Trying to reconnnect..."
                    )
                except:
                    logging.info("Unexpected error. New try in several seconds...")
                    sleep(5)

                wait = min(start_sleep_time * 2**_factor, border_sleep_time)
                _factor += 1
                counter += 1
                sleep(wait)

        return inner

    return func_wrapper
