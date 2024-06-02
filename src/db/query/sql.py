from src.core.configs import RESOURCES

SQL_PATH = RESOURCES / "sql"

with open(file=SQL_PATH / "post_count.sql", encoding="utf-8") as f:
    POST_COUNT_QUERY = f.read()

with open(file=SQL_PATH / "post_list.sql", encoding="utf-8") as f:
    POST_LIST_QUERY = f.read()

with open(file=SQL_PATH / "post_list_keyword_where.sql", encoding="utf-8") as f:
    POST_LIST_QUERY_KEYWORD_WHERE = f.read()

with open(file=SQL_PATH / "post_list_order_limit.sql", encoding="utf-8") as f:
    POST_LIST_QUERY_ORDER_LIMIT = f.read()

with open(file=SQL_PATH / "comment_list.sql", encoding="utf-8") as f:
    COMMENT_LIST_QUERY = f.read()
