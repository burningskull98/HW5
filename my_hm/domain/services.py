from typing import List
from .models import Product, Order, Customer
from .repositories import ProductRepository, OrderRepository, CustomerRepository


class WarehouseService:
    def __init__(
        self,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        customer_repo: CustomerRepository,
    ):
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.customer_repo = customer_repo

    def create_customer(self, name: str, email: str) -> Customer:
        """
        Создает нового клиента и добавляет его в репозиторий.
        """
        customer = Customer(name=name, email=email)
        return self.customer_repo.add(customer)

    def create_product(self, name: str, quantity: int, price: float) -> Product:
        """
        Создает новый продукт и добавляет его в репозиторий.
        """
        product = Product(name=name, quantity=quantity, price=price)
        return self.product_repo.add(product)

    def create_order(self, customer_id: int, product_ids: List[int]) -> Order:
        """
        Создает новый заказ для указанного клиента с выбранными продуктами.
        """
        customer = self.customer_repo.get(customer_id)
        if not customer:
            raise ValueError("Клиент не найден")

        products = []
        for pid in product_ids:
            product = self.product_repo.get(pid)
            if not product or product.quantity <= 0:
                raise ValueError(f"Продукт {pid} недоступен")
            products.append(product)

        order = Order(customer_id=customer_id)
        for product in products:
            order.add_product(product)

        return self.order_repo.add(order)

    def confirm_order(self, order_id: int) -> Order:
        """
        Подтверждает заказ, изменяя его статус и обновляя количество продуктов.
        """
        order = self.order_repo.get(order_id)
        if not order:
            raise ValueError("Заказ не найден")
        order.confirm()
        for product in order.products:
            self.product_repo.update(product)
        self.order_repo.update(order)
        return order

    def ship_order(self, order_id: int) -> Order:
        """
        Отправляет заказ, изменяя его статус и обновляя запись.
        """
        order = self.order_repo.get(order_id)
        if not order:
            raise ValueError("Заказ не найден")
        order.ship()
        self.order_repo.update(order)
        return order

    def cancel_order(self, order_id: int) -> Order:
        """
        Отменяет заказ, изменяя его статус и обновляя количество продуктов.
        """
        order = self.order_repo.get(order_id)
        if not order:
            raise ValueError("Заказ не найден")
        order.cancel()
        for product in order.products:
            self.product_repo.update(product)
        self.order_repo.update(order)
        return order

    def get_available_products(self) -> List[Product]:
        """
        Возвращает список доступных продуктов на складе.
        """
        return [p for p in self.product_repo.list() if p.quantity > 0]
