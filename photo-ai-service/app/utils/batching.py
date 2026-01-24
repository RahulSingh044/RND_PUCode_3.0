from typing import List, Generator, TypeVar

T = TypeVar("T")


def batchify(
    items: List[T],
    batch_size: int
) -> Generator[List[T], None, None]:
    """
    Yield successive batches from a list.

    Args:
        items: List of items to batch
        batch_size: Number of items per batch

    Yields:
        List[T]: A batch of items

    Example:
        for batch in batchify(photos, batch_size=10):
            process(batch)
    """

    if batch_size <= 0:
        raise ValueError("batch_size must be greater than 0")

    total_items = len(items)

    for start in range(0, total_items, batch_size):
        end = start + batch_size
        yield items[start:end]
