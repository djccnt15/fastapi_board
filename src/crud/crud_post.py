from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert, select, update, func, label
from sqlalchemy.orm import aliased

from src.models import *
from src.schemas import PostCreate, SubjectBase


async def read_category_t1_list(db: AsyncSession):
    q = select(PostCategory) \
        .where(PostCategory.tier == 1)
    res = await db.execute(q)
    return res.scalars().all()


async def read_category_list(db: AsyncSession, parent: str):
    tier_1 = aliased(PostCategory)
    q = select(PostCategory) \
        .join(PostCategory.parent.of_type(tier_1)) \
        .where(tier_1.category == parent)
    res = await db.execute(q)
    return res.scalars().all()


async def get_category_id(db: AsyncSession, category: str):
    q = select(PostCategory) \
        .where(PostCategory.category == category)
    res = await db.execute(q)
    return res.scalar()


async def create_post(
        db: AsyncSession,
        id: UUID,
        id_category: int,
        user: User,
        date_create: datetime
):
    q = insert(Post) \
        .values(id=id, id_user=user.id, id_category=id_category, date_create=date_create)
    await db.execute(q)
    await db.commit()


async def create_post_detail(
        db: AsyncSession,
        post_detail: PostCreate,
        id_post: UUID,
        date_upd: datetime = datetime.now(),
        version: int = 0
):
    q = insert(PostContent) \
        .values(
            id=uuid4(),
            version=version,
            date_upd=date_upd,
            subject=post_detail.subject,
            content=post_detail.content,
            id_post=id_post
        )
    await db.execute(q)
    await db.commit()


async def get_post_list(db: AsyncSession, category: str, keyword: str, skip: int, limit: int):
    category_tier_1 = aliased(PostCategory)
    category_subq = select(PostCategory) \
        .join(PostCategory.parent.of_type(category_tier_1)) \
        .where(category_tier_1.category == category) \
        .subquery()
    category = aliased(PostCategory, category_subq, name='category')
    content_subq = select(func.max(PostContent.version), PostContent) \
        .group_by(PostContent.id_post) \
        .subquery()
    content = aliased(PostContent, content_subq, name='content')
    comment_subq = select(label('count_comment', func.count(Comment.id_post)), Comment.id_post) \
        .where(Comment.is_active == True) \
        .group_by(Comment.id_post) \
        .subquery()
    q = select(Post, content, category, User, comment_subq) \
        .join(content) \
        .join(category) \
        .join(User) \
        .outerjoin(comment_subq) \
        .where(Post.is_active == True)
    if keyword:
        keyword = f'%{keyword}%'
        q = q.where(
            content.subject.ilike(keyword) |
            content.content.ilike(keyword) |
            User.username.ilike(keyword)
        )
    q = q.order_by(Post.date_create.desc()) \
        .offset(skip).limit(limit)
    res = await db.execute(q)
    q_t = select(Post, category) \
        .join(category) \
        .where(Post.is_active == True)
    total = await db.execute(select(func.count()).select_from(q_t))
    return total.scalar(), res.all()


async def get_post_detail(db: AsyncSession, id: UUID):
    content_subq = select(func.max(PostContent.version), PostContent) \
        .group_by(PostContent.id_post) \
        .subquery()
    category = aliased(PostCategory, name='category')
    content = aliased(PostContent, content_subq, name='content')
    q = select(Post, content, category, User) \
        .join(content) \
        .join(category) \
        .join(User) \
        .where(
            Post.id == id,
            Post.is_active == True
        )
    res = await db.execute(q)
    return res.first()


async def get_post_ver(db: AsyncSession, id: UUID) -> int:
    q = select(func.max(PostContent.version)) \
        .where(PostContent.id_post == id)
    res = await db.execute(q)
    return res.scalar()


async def get_post(db: AsyncSession, id: UUID):
    q = select(Post) \
        .where(
            Post.id == id,
            Post.is_active == True
        )
    res = await db.execute(q)
    return res.scalar()


async def update_post(db: AsyncSession, id: UUID, ver: int, post_content: SubjectBase):
    q = insert(PostContent) \
        .values(
            id=uuid4(),
            version=ver,
            date_upd=datetime.now(),
            subject=post_content.subject,
            content=post_content.content,
            id_post=id
        )
    await db.execute(q)
    await db.commit()


async def del_post(db: AsyncSession, id: UUID):
    q = update(Post) \
        .where(Post.id == id) \
        .values(is_active = False)
    await db.execute(q)
    await db.commit()


async def get_post_his(db: AsyncSession, id: UUID):
    q = select(PostContent) \
        .where(PostContent.id_post == id)
    res = await db.execute(q)
    return res.scalars().all()