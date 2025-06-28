from typing import Any, Generic, Sequence, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(BaseModel):
    """
    A generic response model for paginated results.
    """

    total_rows: int
    current_page: int
    total_pages: int
    page_size: int
    items: Sequence


class Paginator(Generic[T]):
    """
    A reusable paginator for list-based pagination using Pydantic-compatible models.
    """

    def __init__(self, data: Sequence[Any], page: int = 1, page_size: int = 10, schema: Type[T] | None = None):
        self.data = data
        self.page = max(1, page)
        self.page_size = max(1, page_size)
        self.total_rows = len(data)
        self.schema = schema
        self.total_pages = (self.total_rows + self.page_size - 1) // self.page_size

    def paginate(self):
        """
        Returns the paginated data.
        """
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        raw_items = self.data[start:end]

        if self.schema:
            items = [self.schema.model_validate(raw_item) for raw_item in raw_items]

        else:
            items = raw_items

        return PaginatedResponse(
            total_rows=self.total_rows,
            current_page=self.page,
            total_pages=self.total_pages,
            page_size=self.page_size,
            items=items,
        ).model_dump(mode="json")
