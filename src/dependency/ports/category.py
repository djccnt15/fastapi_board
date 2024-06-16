from abc import ABC, abstractmethod
from typing import Sequence

from src.db.entity.post_entity import PostCategoryEntity


class CategoryRepository(ABC):

    @abstractmethod
    async def read_t1_category_list(self) -> Sequence[PostCategoryEntity]: ...

    @abstractmethod
    async def read_t2_category_list(
        self, *, category: str
    ) -> Sequence[PostCategoryEntity]: ...

    @abstractmethod
    async def read_parent_category(self, *, category: str) -> PostCategoryEntity: ...

    @abstractmethod
    async def read_category_id(self, *, category: str) -> PostCategoryEntity: ...
