from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, functions
from sqlalchemy.orm import aliased

from src.models import User, Post, Comment, CommentContent
from src.schemas import CommentCreate


async def create_comment(
        db: AsyncSession,
        id: UUID,
        post: Post,
        date_create: datetime,
        user: User
):
    q = Comment(id=id, user=user, post=post, date_create=date_create)
    db.add(q)
    await db.commit()


async def create_comment_detail(
        db: AsyncSession,
        comment_detail: CommentCreate,
        id_comment: UUID,
        date_upd: datetime = datetime.now(),
        version: int = 0
):
    q = CommentContent(
        id=uuid4(),
        version=version,
        date_upd=date_upd,
        content=comment_detail.content,
        id_comment=id_comment,
    )
    db.add(q)
    await db.commit()


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