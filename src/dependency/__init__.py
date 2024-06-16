from typing import Annotated

from fastapi import Depends

from . import adapters, ports

UserRepo = Annotated[ports.UserRepository, Depends(adapters.get_user_repo)]
CategoryRepo = Annotated[ports.CategoryRepository, Depends(adapters.get_category_repo)]
PostRepo = Annotated[ports.PostRepository, Depends(adapters.get_post_repo)]
CommentRepo = Annotated[ports.CommentRepository, Depends(adapters.get_comment_repo)]
CacheRepo = Annotated[ports.CacheRepository, Depends(adapters.get_cache_repo)]
IrisInferencer = Annotated[ports.Classifier, Depends(adapters.get_iris_inferencer)]
