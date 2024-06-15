    AND (
        u.name LIKE :keyword
        OR title LIKE :keyword
        OR content LIKE :keyword
    )