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
    JOIN (
        SELECT
            post_id,
            MAX(version) AS max_version
        FROM post_content
        GROUP BY post_id
        ) AS t2 ON t1.post_id = t2.post_id AND t1.version = t2.max_version
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
