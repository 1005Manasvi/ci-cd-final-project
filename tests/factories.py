"""Factories and sample data for product tests."""


def fake_products():
    """Return fresh sample products for tests and BDD scenarios."""
    return [
        {
            "name": "Coffee Maker",
            "category": "Kitchen",
            "price": 49.99,
            "availability": True,
        },
        {
            "name": "Yoga Mat",
            "category": "Fitness",
            "price": 24.5,
            "availability": True,
        },
        {
            "name": "Desk Lamp",
            "category": "Home",
            "price": 18.0,
            "availability": False,
        },
    ]
