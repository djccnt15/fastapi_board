from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import max as SQLMax
from sqlalchemy.sql.expression import label

from src.models.models import User, Post, Category, PostContent


def get_post_list(db: Session, category: str = ''):
    ct1 = db \
        .query(Category.id, Category.name) \
        .filter(Category.name == category) \
        .subquery(name='ct1')
    pcg = db \
        .query(Category.id, Category.name, ct1.c.name) \
        .join(ct1, Category.id_parent == ct1.c.id) \
        .subquery(name='pcg')
    pc1 = db \
        .query(SQLMax(PostContent.version), PostContent.id) \
        .group_by(PostContent.id_post) \
        .subquery(name='pc1')
    pc2 = db \
        .query(PostContent.id_post, PostContent.id, PostContent.date_upd, PostContent.subject) \
        .join(pc1, PostContent.id == pc1.c.id) \
        .subquery(name='pc2')
    post_list = db \
        .query(
            Post.id,
            Post.date_create,
            pc2.c.subject,
            label('category', pcg.c.name),
            label('user', User.username)
        ) \
        .filter(Post.is_active == True) \
        .join(pc2, Post.id == pc2.c.id_post) \
        .join(pcg, Post.id_category == pcg.c.id) \
        .join(User, User.id == Post.id_user)
    total = post_list.distinct().count()
    post_list = post_list \
        .order_by(Post.date_create.desc()) \
        .all()
    return total, post_list