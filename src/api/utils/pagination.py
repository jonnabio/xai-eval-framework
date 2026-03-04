from typing import List, TypeVar, Dict, Any, Tuple

T = TypeVar("T")

def paginate_list(items: List[T], offset: int, limit: int) -> Tuple[List[T], Dict[str, Any]]:
    """
    Paginate a list of items and return the slice plus metadata.

    Args:
        items: List of items to paginate
        offset: Number of items to skip
        limit: Max number of items to return

    Returns:
        Tuple containing:
        - List[T]: The sliced items
        - Dict[str, Any]: Pagination metadata (total, limit, offset, returned, hasNext, hasPrev)
    """
    total = len(items)
    start = offset
    end = min(offset + limit, total)

    if start >= total:
        paginated_items = []
    else:
        paginated_items = items[start:end]

    pagination = {
        "total": total,
        "limit": limit,
        "offset": offset,
        "returned": len(paginated_items),
        "hasNext": end < total,
        "hasPrev": offset > 0
    }

    return paginated_items, pagination
