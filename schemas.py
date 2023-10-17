from typing import Generic, List, Protocol, TypeVar

from django.core.paginator import Paginator
from django.db.models import QuerySet
from pydantic import BaseModel
from pydantic.generics import GenericModel

PaginatedListItem = TypeVar("PaginatedListItem")


class PaginatedList(GenericModel, Generic[PaginatedListItem]):
    items: List[PaginatedListItem]
    limit: int
    total: int
    page: int
    pages: int


class SchemaFactory(Protocol):
    def from_orm(self, model) -> BaseModel:
        pass


def paginate(
    manager_or_qs,
    schema: SchemaFactory,
    page: int = 1,
    limit: int = 50,
    order_by: List[str] = None,
    default_order_by: List[str] = None,
):
    """
    If `order_by` is provided, results will be ordered by `order_by`. Otherwise, if `manager_or_qs` is not already
    ordered, results will be ordered by `default_order_by`, which defaults to `["pk"]`.
    """
    if default_order_by is None:
        default_order_by = ["pk"]
    qs = manager_or_qs if isinstance(manager_or_qs, QuerySet) else manager_or_qs.all()
    if order_by:
        qs = qs.order_by(*order_by)
    elif not qs.query.order_by:
        qs = qs.order_by(*default_order_by)
    paginator = Paginator(qs, limit)
    page = paginator.get_page(page)
    items = [schema.from_orm(f) for f in page.object_list]
    return PaginatedList(
        items=items,
        limit=limit,
        total=paginator.count,
        page=page.number,
        pages=paginator.num_pages,
    )
