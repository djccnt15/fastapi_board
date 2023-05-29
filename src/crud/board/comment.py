from uuid import UUID

from sqlalchemy.sql import select, functions
from sqlalchemy.orm import Session, aliased

from src.models.models import Comment, CommentContent, User


def get_comment_list(db: Session, id_post: UUID):
    content_subq = select(functions.max(CommentContent.version), CommentContent) \
        .group_by(CommentContent.id_comment) \
        .subquery(name="Content")
    Content = aliased(CommentContent, content_subq, name='Content')
    comment = select(Comment, Content, User) \
        .join(Content) \
        .join(User) \
        .where(Comment.id_post == id_post)
    res = db.execute(comment).all()
    return res