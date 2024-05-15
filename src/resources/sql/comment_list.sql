SELECT
    c.id,
    c.created_datetime,
    u.name AS `user`,
    cc.created_datetime AS updated_datetime,
    cc.content,
    vote.vote
FROM comment c
JOIN `user` u ON c.user_id = u.id
JOIN (
    SELECT t1.id, t1.created_datetime, t1.content, t1.comment_id
    FROM comment_content t1
    JOIN (
        SELECT comment_id, max(cc.version) AS last
        FROM comment_content cc
        GROUP BY cc.comment_id
    ) t2 ON t1.comment_id = t2.comment_id AND t1.version = t2.last
) AS cc ON c.id = cc.comment_id
LEFT JOIN (
    SELECT voter_comment.comment_id AS comment_id, count(*) AS vote
    FROM voter_comment
    GROUP BY voter_comment.comment_id
) vote ON c.id = vote.comment_id
WHERE
    c.is_active = TRUE
    AND c.post_id = :post_id
ORDER BY id