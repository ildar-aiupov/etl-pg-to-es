select_data = """
    SELECT genre.id, genre.name
    FROM genre
    WHERE genre.id IN %s;
    """

select_ids = """
    SELECT genre.id
    FROM genre
    WHERE genre.modified > %s;
    """
