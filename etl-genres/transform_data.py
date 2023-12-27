import json


def extract_properties(data):
    genre_id = data["id"]
    genre_name = json.dumps(data["name"])
    return (
        "{" + f'"uuid": "{genre_id}",'
        f'"name": {genre_name}' + "}"
    )
