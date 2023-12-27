import datetime
import sys
import os
import logging
import time

from dotenv import load_dotenv

from transform_data import extract_properties
from state import State
from elastic import Elastic
from postgres import Postgres


def main():
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        encoding="utf8",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    pg_params = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
        "options": os.environ.get("OPTIONS"),
    }
    es_params = {
        "es_host": os.environ.get("ES_HOST", default="elastic"),
        "es_port": os.environ.get("ES_PORT", default="9200"),
        "index_name": os.environ.get("INDEX_NAME_PERSONS", default="persons"),
    }

    state = State("last_updated")
    if not state.get_last_update():
        state.save_last_update(datetime.datetime.min)

    elastic = Elastic(**es_params)
    elastic.create_es_index()

    while True:
        try:
            postgres = Postgres(pg_params)
            logging.info("Checking updates...")
            new_entries = postgres.check_updates(state)
            if not new_entries:
                logging.info("There is no updates. Waiting for updates. Pause...")
                time.sleep(15)
                continue
            logging.info(f"Found {new_entries} updates. Updation begins...")
            last_update = datetime.datetime.utcnow()
            count = 0
            for portion in postgres.load_portion():
                for entry in portion:
                    entry = dict(entry)
                    properties = extract_properties(entry)
                    entry_id = entry["id"]
                    response = elastic.save_to_es(properties, entry_id)
                    count += 1
                    if response.status_code in [200, 201]:
                        logging.info(
                            f"Updated {count} entries. Response code = {response.status_code}"
                        )
                    else:
                        logging.info(
                            f"Entry with id={entry_id} is not updated. "
                            f"Response code = {response.status_code}. "
                            f"Response text = {response.text}"
                        )

            logging.info("Updation completed")
            state.save_last_update(last_update)

        finally:
            if not postgres.connection.closed:
                postgres.connection.close()


if __name__ == "__main__":
    main()
