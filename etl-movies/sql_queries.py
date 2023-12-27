select_data = """
    SELECT
    film_work.id,
    film_work.title,
    film_work.rating,
    film_work.description,
    ARRAY_AGG (DISTINCT genre.id || '$' || genre.name) as genres,
    ARRAY_AGG (DISTINCT person.id || '$' || person.full_name) FILTER (WHERE person_film_work.role='actor') as actors,
    ARRAY_AGG (DISTINCT person.id || '$' || person.full_name) FILTER (WHERE person_film_work.role='writer') as writers,
    ARRAY_AGG (DISTINCT person.id || '$' || person.full_name) FILTER (WHERE person_film_work.role='director') as directors
    
    FROM film_work
    LEFT JOIN person_film_work ON film_work.id=person_film_work.film_work_id
    LEFT JOIN person ON person.id=person_film_work.person_id
    LEFT JOIN genre_film_work ON film_work.id=genre_film_work.film_work_id
    LEFT JOIN genre ON genre.id=genre_film_work.genre_id
    WHERE film_work.id IN %s
    GROUP BY film_work.id;
    """

select_ids = """
    SELECT
    DISTINCT film_work.id
    FROM film_work
    LEFT JOIN person_film_work ON film_work.id=person_film_work.film_work_id
    LEFT JOIN person ON person.id=person_film_work.person_id
    LEFT JOIN genre_film_work ON film_work.id=genre_film_work.film_work_id
    LEFT JOIN genre ON genre.id=genre_film_work.genre_id
    WHERE GREATEST(person.modified, genre.modified, film_work.modified) > %s;
    """
