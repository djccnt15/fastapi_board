from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update, functions
from sqlalchemy.orm import aliased

from src.models import User, Post, Comment, CommentContent
from src.schemas import ContentBase


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
        comment_detail: ContentBase,
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


async def get_comment_list(db: AsyncSession, id: UUID):
    content_subq = select(functions.max(CommentContent.version), CommentContent) \
        .group_by(CommentContent.id_comment) \
        .subquery(name='Content')
    Content = aliased(CommentContent, content_subq, name='Content')
    q = select(Comment, Content, User) \
        .join(Content) \
        .join(User) \
        .where(Comment.id_post == id) \
        .order_by(Comment.date_create)
    res = await db.execute(q)
    return res.all()


async def get_comment_ver(db: AsyncSession, id: UUID) -> int:
    q = select(functions.max(CommentContent.version)) \
        .where(CommentContent.id_comment == id)
    res = await db.execute(q)
    return res.scalar()


async def get_commented_post(db: AsyncSession, id: UUID):
    q = select(Comment) \
        .where(Comment.id_post == id)
    res = await db.execute(q)
    return res.scalar()


async def get_comment(db: AsyncSession, id: UUID):
    q = select(Comment) \
        .where(Comment.id == id)
    res = await db.execute(q)
    return res.scalar()


async def update_comment(db: AsyncSession, id: UUID, ver: int, comment_content: ContentBase):
    q = CommentContent(
        id=uuid4(),
        version=ver,
        date_upd=datetime.now(),
        content=comment_content.content,
        id_comment=id
    )
    db.add(q)
    await db.commit()


async def del_comment(db: AsyncSession, id: UUID):
    q = update(Comment) \
        .where(Comment.id == id) \
        .values(is_active = False)
    await db.execute(q)
    await db.commit()


async def get_comment_his(db: AsyncSession, id: UUID):
    q = select(CommentContent) \
        .where(CommentContent.id_comment == id)
    res = await db.execute(q)
    return res.scalars().all()