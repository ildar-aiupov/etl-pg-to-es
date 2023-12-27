import logging
from pip._vendor import requests

from backoff import backoff


class Elastic:
    def __init__(self, es_host, es_port, index_name):
        self.index_name = index_name
        self.url = f"http://{es_host}:{es_port}/{index_name}"

    @backoff()
    def create_es_index(self):
        with open("index_config", "r") as f:
            data = f.read()
        response = requests.put(
            url=self.url,
            headers={"Content-Type": "application/json"},
            data=data,
        )
        if response.status_code == 200:
            logging.info(f"Elasticsearch index '{self.index_name}' created")
        else:
            logging.info(f"Elasticsearch index '{self.index_name}' already exists")

    @backoff()
    def save_to_es(self, properties, entry_id):
        return requests.post(
            url=f"{self.url}/_doc/{entry_id}",
            headers={"Content-Type": "application/json; charset=UTF-8'"},
            data=properties,
        )
