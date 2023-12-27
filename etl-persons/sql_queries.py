select_data = """
    SELECT
    id,
    full_name,
    ARRAY_AGG (DISTINCT fw_id || '$' || ARRAY_TO_STRING(roles, ',')) as films
    
    FROM
    (
    SELECT
    person.id as id,
    person.full_name as full_name,
    film_work.id as fw_id,
    ARRAY_AGG (DISTINCT person_film_work.role) as roles
        
    FROM person
    LEFT JOIN person_film_work ON person.id=person_film_work.person_id
    LEFT JOIN film_work ON film_work.id=person_film_work.film_work_id

    WHERE person.id IN %s
    GROUP BY person.id, film_work.id
    ) as s

    GROUP BY id, full_name;
    """

select_ids = """
    SELECT DISTINCT person.id
    FROM person
    LEFT JOIN person_film_work ON person.id=person_film_work.person_id
    LEFT JOIN film_work ON film_work.id=person_film_work.film_work_id
    WHERE person.modified > %s;
    """
