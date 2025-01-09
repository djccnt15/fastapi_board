SELECT COUNT(*)
FROM post AS p
JOIN category AS c ON p.category_id = c.id
JOIN (
    SELECT
        t1.id,
        t1.created_datetime,
        t1.title,
        t1.content,
        t1.post_id
    FROM post_content AS t1
    WHERE t1.version = (
        SELECT MAX(version)
        FROM post_content AS t2
        WHERE t1.post_id = t2.post_id
    )
) AS pc ON p.id = pc.post_id
WHERE
    p.is_active = TRUE
    AND (
        c.parent_id = :category_id
        OR c.id = :category_id
    )
    AND (
        title LIKE :keyword
        OR content LIKE :keyword
    )
