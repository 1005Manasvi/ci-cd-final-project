"""Web/API interaction and response assertion steps for product scenarios."""

from behave import given, then, when


@given('I filter by {field} "{value}"')
def set_product_filter(context, field, value):
    """Set a product-list query filter for the next search."""
    context.filters[field] = value


@when('I click the "{button}" button')
def click_button(context, button):
    """Exercise a product API action represented by a UI button."""
    actions = {
        "read": lambda: context.client.get(
            "/products/{}".format(context.product.id)
        ),
        "delete": lambda: context.client.delete(
            "/products/{}".format(context.product.id)
        ),
        "list all": lambda: context.client.get("/products"),
        "search": lambda: context.client.get("/products", query_string=context.filters),
    }
    action = actions.get(button.casefold())
    if action is None:
        raise AssertionError("Unsupported button: {}".format(button))
    context.response = action()


@when('I update the product name to "{name}"')
def update_product_name(context, name):
    """Update the selected product and store the API response."""
    context.response = context.client.put(
        "/products/{}".format(context.product.id),
        json={"name": name},
    )


@then('the text "{text}" should be present')
def verify_text_present(context, text):
    """Assert that the response contains the expected product text."""
    assert text in context.response.get_data(as_text=True)


@then('the text "{text}" should not be present')
def verify_text_not_present(context, text):
    """Assert that the response does not contain a removed/unmatched product."""
    assert text not in context.response.get_data(as_text=True)


@then('I should see message "{message}"')
def verify_message(context, message):
    """Assert that the API returned the expected success message."""
    assert context.response.headers.get("X-Message") == message
