from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import max as SQLMax

from src.models.models import User, Comment, CommentContent


def get_comment_list(db: Session, id_post: int):
    comment_last_upd = db \
        .query(
            SQLMax(CommentContent.version),
            CommentContent.id,
            CommentContent.id_comment,
            CommentContent.version,
            CommentContent.date_upd,
            CommentContent.content
        ) \
        .group_by(CommentContent.id_comment) \
        .subquery(name='comment_last_upd')
    comment = db \
        .query(
            Comment.id, Comment.date_create,
            comment_last_upd.c.version, comment_last_upd.c.date_upd, comment_last_upd.c.content,
            User.username, User.is_superuser, User.is_staff, User.is_staff, User.is_blocked, User.is_active
        ) \
        .join(comment_last_upd, Comment.id == comment_last_upd.c.id_comment) \
        .join(User, Comment.user) \
        .filter(Comment.id_post == id_post) \
        .filter(Comment.is_active == True) \
        .order_by(Comment.date_create) \
        .all()
    return comment