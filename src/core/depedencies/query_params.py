from typing import Any

from fastapi import Request
from src.core.schemas.common import QueryParams


class CommonQueryParam:
    def __init__(
        self,
        filter_fields: list[str] | None = None,
    ) -> None:
        self.filter_fields = filter_fields
        self.sorting: dict[Any, Any] | None = None

    def __call__(
        self,
        request: Request,
        search: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> QueryParams:
        data = {
            "search": search,
            "page": page,
            "page_size": page_size,
            "sorting": self.sorting,
        }

        query_clone = dict(request.query_params).copy()
        entries_to_remove = ("page", "page_size", "search")
        for key in entries_to_remove:
            query_clone.pop(key, None)

        filter_params: dict[str, Any] = {}
        for key, value in query_clone.items():
            if self.filter_fields is None or key in self.filter_fields:  # noqa: SIM102
                if value not in (None, ""):
                    filter_params[key] = value

        if query_clone.get("order_by_fields"):  # {"order_by_fields": "date", "ordering: "desc"}
            data["sorting"] = {
                query_clone.get("order_by_fields"): query_clone.get("ordering", "desc")
            }

        data["filter_params"] = filter_params

        return QueryParams(**data)
