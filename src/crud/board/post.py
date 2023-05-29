from sqlalchemy.sql import select
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql.functions import max as MAX
from sqlalchemy.orm import Session

from src.models.models import User, Post, Category, PostContent


def create_post(db: Session):
    ...


def get_post_list(db: Session, category: str = ''):
    category_tier_1 = aliased(Category)
    category_list = select(Category) \
        .join(Category.parent.of_type(category_tier_1)) \
        .where(category_tier_1.category == category) \
        .subquery(name='category_list')
    post_category = select(Post) \
        .join(category_list, Post.id_category == category_list.c.id) \
        .subquery(name='post_category')
    post_last_upd = select(MAX(PostContent.version), PostContent.id) \
        .group_by(PostContent.id_post) \
        .subquery(name='post_last_upd')
    content_subq = select(PostContent) \
        .join(post_last_upd, PostContent.id == post_last_upd.c.id) \
        .subquery(name='Content')
    Content = aliased(PostContent, content_subq, name='Content')
    post_list = select(Post, Content, Category, User) \
        .join(Content) \
        .join(post_category, post_category.c.id == Post.id) \
        .join(Category) \
        .join(User) \
        .where(Post.is_active == True) \
        .order_by(Post.date_create.desc())
    result = db.execute(post_list).all()
    total = len(result)
    return total, result


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