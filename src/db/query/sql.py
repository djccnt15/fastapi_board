from src.common.configs import RESOURCES

path = RESOURCES / "sql"

with open(file=path / "post_count.sql", encoding="utf-8") as f:
    POST_COUNT_QUERY = f.read()

with open(file=path / "post_list.sql", encoding="utf-8") as f:
    POST_LIST_QUERY = f.read()

with open(file=path / "post_list_keyword_where.sql", encoding="utf-8") as f:
    POST_LIST_QUERY_KEYWORD_WHERE = f.read()

with open(file=path / "post_list_order_limit.sql", encoding="utf-8") as f:
    POST_LIST_QUERY_ORDER_LIMIT = f.read()

with open(file=path / "comment_list.sql", encoding="utf-8") as f:
    COMMENT_LIST_QUERY = f.read()
