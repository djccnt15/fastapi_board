SELECT
    p.id,
    p.created_datetime,
    pc.created_datetime AS updated_datetime,
    c.name AS category,
    u.name AS `user`,
    pc.title,
    pc.content,
    comment.comment,
    vote.vote
FROM post AS p
JOIN category c ON p.category_id = c.id
JOIN `user` u ON p.user_id = u.id
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
LEFT JOIN (
    SELECT c.post_id, COUNT(*) AS comment
    FROM comment c
    WHERE
        c.is_active = TRUE
    GROUP BY post_id
) AS comment ON p.id = comment.post_id
LEFT JOIN (
    SELECT
        voter_post.post_id,
        count(*) AS vote
    FROM voter_post
    GROUP BY voter_post.post_id
) AS vote ON p.id = vote.post_id
WHERE
    p.is_active = TRUE
    AND (
        c.parent_id = :category_id
        OR c.id = :category_id
    )
    AND (
        u.name LIKE :keyword
        OR title LIKE :keyword
        OR content LIKE :keyword
    )
ORDER BY p.id DESC
LIMIT :size OFFSET :page
