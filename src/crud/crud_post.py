from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, functions, func
from sqlalchemy.orm import aliased

from src.models import User, PostCategory, Post, PostContent
from src.schemas import PostCreate, PostContentBase


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
    q = Post(id=id, id_category=id_category, date_create=date_create, user=user)
    db.add(q)
    await db.commit()


async def create_post_detail(
        db: AsyncSession,
        post_detail: PostCreate,
        id_post: UUID,
        date_upd: datetime = datetime.now(),
        version: int = 0
):
    q = PostContent(
        id=uuid4(),
        version=version,
        date_upd=date_upd,
        subject=post_detail.subject,
        content=post_detail.content,
        id_post=id_post
    )
    db.add(q)
    await db.commit()


async def get_post_list(db: AsyncSession, category: str, keyword: str, skip: int, limit: int):
    category_tier_1 = aliased(PostCategory)
    category_subq = select(PostCategory) \
        .join(PostCategory.parent.of_type(category_tier_1)) \
        .where(category_tier_1.category == category) \
        .subquery(name='category_subq')
    Category = aliased(PostCategory, category_subq, name='Category')
    content_subq = select(functions.max(PostContent.version), PostContent) \
        .group_by(PostContent.id_post) \
        .subquery(name='Content')
    Content = aliased(PostContent, content_subq, name='Content')
    q = select(Post, Content, Category, User) \
        .join(Content) \
        .join(Category) \
        .join(User) \
        .where(Post.is_active == True)
    if keyword:
        keyword = f'%{keyword}%'
        q = q.where(
            Content.subject.ilike(keyword) |
            Content.content.ilike(keyword) |
            User.username.ilike(keyword)
        )
    total = await db.execute(select(func.count()).select_from(q))
    q = q.order_by(Post.date_create.desc()) \
        .offset(skip).limit(limit)
    res = await db.execute(q)
    return total.scalar(), res.all()


async def get_post_detail(db: AsyncSession, id: UUID):
    content_subq = select(functions.max(PostContent.version), PostContent) \
        .group_by(PostContent.id_post) \
        .subquery(name='Content')
    Category = aliased(PostCategory, name='Category')
    Content = aliased(PostContent, content_subq, name='Content')
    q = select(Post, Content, Category, User) \
        .join(Content) \
        .join(Category) \
        .join(User) \
        .where(Post.id == id)
    res = await db.execute(q)
    return res.first()


async def get_content_ver(db: AsyncSession, id: UUID) -> int:
    q = select(functions.max(PostContent.version)) \
        .where(PostContent.id_post == id)
    res = await db.execute(q)
    return res.scalar()


async def get_post(db: AsyncSession, id: UUID):
    q = select(Post) \
        .where(Post.id == id)
    res = await db.execute(q)
    return res.scalar()


async def update_post(db: AsyncSession, id: UUID, ver: int, post_content: PostContentBase):
    q = PostContent(
        id=uuid4(),
        version=ver,
        date_upd=datetime.now(),
        subject=post_content.subject,
        content=post_content.content,
        id_post=id
    )
    db.add(q)
    await db.commit()


async def del_post(db: AsyncSession):  # WIP
    ...