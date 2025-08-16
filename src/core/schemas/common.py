from typing import Any

from pydantic import BaseModel, Field


class QueryParams(BaseModel):
    page: int = Field(1, ge=1, description="The page number to retrieve")
    page_size: int = Field(10, ge=1, le=100, description="The number of items per page")
    search: str | None = Field(None, description="The search query")
    filter_params: dict[str, Any] | None = None
    sorting: dict[str, str] | None = None

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size


class FilterOptions(BaseModel):
    filters: dict[str, Any]
    pagination: QueryParams | None = None
    search_fields: list[str] | None = None
    sorting: dict[str, str] | None = None
    prefetch: tuple[str, ...] | None = None

    use_or: bool = False
    distinct_on: str | None = None
    # raw_query: str | None = None
    or_filters: set[str] | None = None
