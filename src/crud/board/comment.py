from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, functions
from sqlalchemy.orm import aliased

from src.models.models import Comment, CommentContent, User


async def get_comment_list(db: AsyncSession, id_post: UUID):
    content_subq = select(functions.max(CommentContent.version), CommentContent) \
        .group_by(CommentContent.id_comment) \
        .subquery(name="Content")
    Content = aliased(CommentContent, content_subq, name='Content')
    q = select(Comment, Content, User) \
        .join(Content) \
        .join(User) \
        .where(Comment.id_post == id_post)
    res = await db.execute(q)
    return res.all()