import json


def extract_properties(data):
    person_id = data["id"]
    full_name = json.dumps(data["full_name"])
    films = json.dumps(
        [
            {"uuid": id, "roles": roles.split(",")}
            for (id, roles) in [
                (id_roles.split("$")[0], id_roles.split("$")[1])
                for id_roles in data["films"] or []
            ]
        ]
    )
    return (
        "{" + f'"uuid": "{person_id}",'
        f'"full_name": {full_name},'
        f'"films": {films}' + "}"
    )
