"""Steps that prepare product data for BDD scenarios."""

from behave import given

from service import app
from service.models import Product


@given("the following products")
def load_products(context):
    """Load the scenario's product table into the in-memory model."""
    Product.clear()
    context.client = app.test_client()
    context.products = {}
    for row in context.table:
        product = Product.create(
            name=row["name"].strip(),
            category=row["category"].strip(),
            price=float(row["price"]),
            availability=row["availability"].strip().casefold() == "true",
        )
        context.products[product.name] = product
    context.product = next(iter(context.products.values()))
    context.response = None
    context.filters = {}
