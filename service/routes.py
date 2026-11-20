"""
Controller for routes
"""
from flask import jsonify, url_for, abort, request
from service import app
from service.common import status
from service.models import Product

COUNTER = {}


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


############################################################
# Index page
############################################################
@app.route("/")
def index():
    """Returns information abut the service"""
    app.logger.info("Request for Base URL")
    return jsonify(
        status=status.HTTP_200_OK,
        message="Hit Counter Service",
        version="1.0.0",
        url=url_for("list_counters", _external=True),
    )


############################################################
# List counters
############################################################
@app.route("/counters", methods=["GET"])
def list_counters():
    """Lists all counters"""
    app.logger.info("Request to list all counters...")

    counters = [dict(name=count[0], counter=count[1]) for count in COUNTER.items()]

    return jsonify(counters)


############################################################
# Create counters
############################################################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Creates a new counter"""
    app.logger.info("Request to Create counter: %s...", name)

    if name in COUNTER:
        return abort(status.HTTP_409_CONFLICT, f"Counter {name} already exists")

    COUNTER[name] = 0

    location_url = url_for("read_counters", name=name, _external=True)
    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# Read counters
############################################################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Reads a single counter"""
    app.logger.info("Request to Read counter: %s...", name)

    if name not in COUNTER:
        return abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")

    counter = COUNTER[name]
    return jsonify(name=name, counter=counter)


############################################################
# Update counters
############################################################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Updates a counter"""
    app.logger.info("Request to Update counter: %s...", name)

    if name not in COUNTER:
        return abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")

    COUNTER[name] += 1

    counter = COUNTER[name]
    return jsonify(name=name, counter=counter)


############################################################
# Delete counters
############################################################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Deletes a counter"""
    app.logger.info("Request to Delete counter: %s...", name)

    if name in COUNTER:
        COUNTER.pop(name)

    return "", status.HTTP_204_NO_CONTENT


############################################################
# Product API
############################################################
def _product_error(message, http_status):
    """Return a JSON API error response."""
    return jsonify(error=message), http_status


def _product_message(message):
    """Build the standard success-message response header."""
    return {"X-Message": message}


def _parse_availability(value):
    """Convert a query-string boolean to a boolean, or return None."""
    normalized = value.casefold()
    if normalized in ("true", "1", "yes"):
        return True
    if normalized in ("false", "0", "no"):
        return False
    return None


def _is_valid_product_field(field, value):
    """Validate a product field value."""
    if field in ("name", "category"):
        return isinstance(value, str) and bool(value.strip())
    if field == "price":
        return (
            not isinstance(value, bool)
            and isinstance(value, (int, float))
        )
    return isinstance(value, bool)


def _valid_product_attributes(attributes, required=()):
    """Validate product fields and any required field names."""
    if not isinstance(attributes, dict) or any(
        field not in attributes for field in required
    ):
        return False
    allowed = {"name", "category", "price", "availability"}
    if set(attributes) - allowed:
        return False
    return all(
        _is_valid_product_field(field, value)
        for field, value in attributes.items()
    )


@app.route("/products", methods=["POST"])
def create_product():
    """Create a product from a JSON request."""
    if not request.is_json:
        return _product_error("A JSON request body is required", status.HTTP_400_BAD_REQUEST)
    required = ("name", "category", "price", "availability")
    attributes = request.get_json(silent=True)
    if not _valid_product_attributes(attributes, required):
        return _product_error(
            "name, category, price, and availability are required",
            status.HTTP_400_BAD_REQUEST,
        )
    product = Product.create(
        name=attributes["name"].strip(),
        category=attributes["category"].strip(),
        price=attributes["price"],
        availability=attributes["availability"],
    )
    return (
        jsonify(product.serialize()),
        status.HTTP_201_CREATED,
        _product_message("Product created successfully"),
    )


@app.route("/products", methods=["GET"])
def list_products():
    """List all products, optionally filtered by name, category, or availability."""
    products = Product.all()
    if "name" in request.args:
        products = Product.find_by_name(request.args["name"])
    if "category" in request.args:
        products = [
            product for product in products
            if product in Product.find_by_category(request.args["category"])
        ]
    if "availability" in request.args:
        availability = _parse_availability(request.args["availability"])
        if availability is None:
            return _product_error(
                "availability must be true or false",
                status.HTTP_400_BAD_REQUEST,
            )
        products = [
            product for product in products
            if product in Product.find_by_availability(availability)
        ]
    return (
        jsonify([product.serialize() for product in products]),
        status.HTTP_200_OK,
        _product_message("Products retrieved successfully"),
    )


@app.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id):
    """Read one product by identifier."""
    product = Product.find(product_id)
    if product is None:
        return _product_error("Product not found", status.HTTP_404_NOT_FOUND)
    return (
        jsonify(product.serialize()),
        status.HTTP_200_OK,
        _product_message("Product retrieved successfully"),
    )


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update fields on an existing product."""
    if not request.is_json:
        return _product_error("A JSON request body is required", status.HTTP_400_BAD_REQUEST)
    attributes = request.get_json(silent=True)
    if not attributes:
        return _product_error("At least one product field is required", status.HTTP_400_BAD_REQUEST)
    if not _valid_product_attributes(attributes):
        return _product_error("Invalid product fields", status.HTTP_400_BAD_REQUEST)
    if "name" in attributes:
        attributes["name"] = attributes["name"].strip()
    if "category" in attributes:
        attributes["category"] = attributes["category"].strip()
    product = Product.update(product_id, **attributes)
    if product is None:
        return _product_error("Product not found", status.HTTP_404_NOT_FOUND)
    return (
        jsonify(product.serialize()),
        status.HTTP_200_OK,
        _product_message("Product updated successfully"),
    )


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product by identifier."""
    if not Product.delete(product_id):
        return _product_error("Product not found", status.HTTP_404_NOT_FOUND)
    return "", status.HTTP_204_NO_CONTENT, _product_message("Product deleted successfully")


############################################################
# Utility for testing
############################################################
def reset_counters():
    """Removes all counters while testing"""
    global COUNTER  # pylint: disable=global-statement
    if app.testing:
        COUNTER = {}
