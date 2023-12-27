import json


def extract_properties(data):
    film_work_id = data["id"]
    title = json.dumps(data["title"])
    imdb_rating = data["rating"] or "null"
    description = json.dumps(data["description"])

    genres = json.dumps(
        [
            {"uuid": id, "name": name}
            for (id, name) in [
                (id_name.split("$")[0], id_name.split("$")[1])
                for id_name in data["genres"] or []
            ]
        ]
    )

    actors = json.dumps(
        [
            {"uuid": id, "full_name": name}
            for (id, name) in [
                (id_name.split("$")[0], id_name.split("$")[1])
                for id_name in data["actors"] or []
            ]
        ]
    )

    writers = json.dumps(
        [
            {"uuid": id, "full_name": name}
            for (id, name) in [
                (id_name.split("$")[0], id_name.split("$")[1])
                for id_name in data["writers"] or []
            ]
        ]
    )

    directors = json.dumps(
        [
            {"uuid": id, "full_name": name}
            for (id, name) in [
                (id_name.split("$")[0], id_name.split("$")[1])
                for id_name in data["directors"] or []
            ]
        ]
    )

    return (
        "{" + f'"uuid": "{film_work_id}",'
        f'"title": {title},'
        f'"imdb_rating": {imdb_rating},'
        f'"description": {description},'
        f'"genre": {genres},'
        f'"actors": {actors},'
        f'"writers": {writers},'
        f'"directors": {directors}' + "}"
    )
