"""In-memory product model used by the product API."""


class Product:
    """A product and the in-memory operations used to manage products."""

    _products = {}
    _next_id = 1

    def __init__(self, name, category, price, availability, product_id):
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.availability = availability

    def serialize(self):
        """Return the public representation of a product."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "availability": self.availability,
        }

    @classmethod
    def create(cls, name, category, price, availability):
        """Create and store a product."""
        product = cls(name, category, price, availability, cls._next_id)
        cls._products[product.id] = product
        cls._next_id += 1
        return product

    @classmethod
    def all(cls):
        """Return all products in insertion order."""
        return list(cls._products.values())

    @classmethod
    def find(cls, product_id):
        """Find a product by its identifier."""
        return cls._products.get(product_id)

    @classmethod
    def update(cls, product_id, **attributes):
        """Update an existing product and return it, or None if absent."""
        product = cls.find(product_id)
        if product is None:
            return None
        for attribute, value in attributes.items():
            setattr(product, attribute, value)
        return product

    @classmethod
    def delete(cls, product_id):
        """Delete a product and return whether it existed."""
        return cls._products.pop(product_id, None) is not None

    @classmethod
    def find_by_name(cls, name):
        """Find products whose names contain the supplied text."""
        query = name.casefold()
        return [product for product in cls.all() if query in product.name.casefold()]

    @classmethod
    def find_by_category(cls, category):
        """Find products in a category, ignoring letter case."""
        query = category.casefold()
        return [
            product for product in cls.all()
            if product.category.casefold() == query
        ]

    @classmethod
    def find_by_availability(cls, availability):
        """Find products with the requested availability."""
        return [
            product for product in cls.all()
            if product.availability is availability
        ]

    @classmethod
    def clear(cls):
        """Remove all products and reset identifiers."""
        cls._products = {}
        cls._next_id = 1
