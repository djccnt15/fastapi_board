from uuid import UUID

from sqlalchemy.sql import select, functions
from sqlalchemy.orm import Session, aliased

from src.models.models import User, Post, PostCategory, PostContent


def create_post(db: Session):
    ...


def get_post_list(db: Session, category: str = ''):
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
    post_list = select(Post, Content, Category, User) \
        .join(Content) \
        .join(Category) \
        .join(User) \
        .where(Post.is_active == True) \
        .order_by(Post.date_create.desc())
    result = db.execute(post_list).all()
    total = len(result)
    return total, result


def get_post(db: Session, id_post: UUID):
    content_subq = select(functions.max(PostContent.version), PostContent) \
        .group_by(PostContent.id_post) \
        .subquery(name='Content')
    Category = aliased(PostCategory, name='Category')
    Content = aliased(PostContent, content_subq, name='Content')
    post = select(Post, Content, Category, User) \
        .join(Content) \
        .join(Category) \
        .join(User) \
        .where(Post.id == id_post)
    res = db.execute(post).first()
    return res


def update_post(db: Session):
    ...


def del_post(db: Session):
    ...