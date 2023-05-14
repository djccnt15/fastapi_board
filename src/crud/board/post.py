from sqlalchemy.orm import Session
from sqlalchemy.sql import functions

from src.models.models import User, Post, Category, PostContent


def create_post(db: Session):
    ...


def get_post_list(db: Session, category: str = ''):
    category_tier_1 = db \
        .query(Category.id, Category.category) \
        .filter(Category.category == category) \
        .subquery(name='category_tier_1')
    post_category = db \
        .query(Category.id, Category.category,
               category_tier_1.c.category) \
        .join(category_tier_1, Category.id_parent == category_tier_1.c.id) \
        .subquery(name='post_category')
    post_last_upd = db \
        .query(functions.max(PostContent.version), PostContent.id) \
        .group_by(PostContent.id_post) \
        .subquery(name='post_last_upd')
    post_content = db \
        .query(PostContent.id_post, PostContent.id, PostContent.date_upd, PostContent.subject) \
        .join(post_last_upd, PostContent.id == post_last_upd.c.id) \
        .subquery(name='post_content')
    post_list = db \
        .query(
            Post.id, Post.date_create,
            post_content.c.subject,
            post_category.c.category,
            User.username
        ) \
        .filter(Post.is_active == True) \
        .join(post_content, Post.id == post_content.c.id_post) \
        .join(post_category, Post.id_category == post_category.c.id) \
        .join(User, Post.user)
    total = post_list.distinct().count()
    post_list = post_list \
        .order_by(Post.id.desc()) \
        .all()
    return total, post_list


def get_post(db: Session, id_post: int):
    post = db.get(Post, id_post)
    return post


def get_post_content(db: Session, id_post: int):
    content = db \
        .query(PostContent) \
        .filter(PostContent.id_post == id_post) \
        .order_by(PostContent.version.desc()) \
        .first()
    return content


def update_post(db: Session):
    ...


def del_post(db: Session):
    ...