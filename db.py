from uuid import UUID, uuid4

# Task 3.2
class ProductsStorage:
    def __init__(self):
        self.PRODUCTS = [
            {
                "product_id": 123,
                "name": "Smartphone",
                "category": "Electronics",
                "price": 599.99
            },
            {
                "product_id": 456,
                "name": "Phone Case",
                "category": "Accessories",
                "price": 19.99
            },
            {
                "product_id": 789,
                "name": "Iphone",
                "category": "Electronics",
                "price": 1299.99
            },
            {
                "product_id": 101,
                "name": "Headphones",
                "category": "Accessories",
                "price": 99.99
            },
            {
                "product_id": 202,
                "name": "Smartwatch",
                "category": "Electronics",
                "price": 299.99
            },
        ]

    def get_product(self, product_id: int) -> dict | None:
        for product in self.PRODUCTS:
            if product["product_id"] == product_id:
                return product

    def search_products(self, keyword: str, category: str | None = None, limit: int = 10) -> list[dict]:
        res = []

        for product in self.PRODUCTS:
            m1 = keyword.lower() in product["name"].lower()
            m2 = True if category is None else product["category"].lower() == category.lower()

            if m1 and m2:
                res.append(product)

            if len(res) >= limit:
                break

        return res

# Task 5.1
class UsersStorage:
    def __init__(self):
        self.USERS = [
            {
                "user_id": UUID("3f8f4f8e-3a2d-4a5b-8c1d-1b2c3d4e5f60"),
                "password": "password123",
                "username": "Alice",
                "email": "alice@example.com"
            },
            {
                "user_id": UUID("7c1a9d20-5b6f-4c1e-9d2a-6e7f8a9b0c11"),
                "password": "qwerty202",
                "username": "Mike",
                "email": "mike@example.com"
            },
        ]

        self.SESSIONS = {}

    def check_user(self, username: str, password: str) -> dict | None:
        for user in self.USERS:
            if user["username"] == username and user["password"] == password:
                return user
        return None

    def create_session(self, user_id:UUID):
        token = uuid4()
        self.SESSIONS[token] = user_id
        return token

    def get_user_by_id(self, user_id: UUID) -> dict | None:
        for user in self.USERS:
            if user["user_id"] == user_id:
                return user
        return None

    def get_user(self, session:UUID) -> dict | None:
        user_id = self.SESSIONS.get(session)
        return self.get_user_by_id(user_id)
