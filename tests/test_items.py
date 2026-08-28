from src.items.item import Item


def test_valid_item():
    item = Item(
        item_id=1,
        workload=2.5,
        priority=2,
    )

    assert item.item_id == 1
    assert item.workload == 2.5


def test_invalid_item():
    try:
        Item(
            item_id=1,
            workload=0,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
