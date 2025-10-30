from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


@dataclass
class Customer:
    id: Optional[int] = None
    name: str = ""
    email: str = ""


@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    quantity: int = 0
    price: float = 0.0

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Количество не может быть отрицательным числом")
        if self.price <= 0:
            raise ValueError("Цена должна быть положительным числом")


@dataclass
class Order:
    id: Optional[int] = None
    customer_id: Optional[int] = None
    products: List[Product] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    total_price: float = 0.0

    def add_product(self, product: Product, quantity: int = 1):
        """
        Добавляет продукт в заказ, уменьшая его количество в наличии.
        """
        if product.quantity < quantity:
            raise ValueError(f"Недостаточно {product.name} на складе")
        product.quantity -= quantity
        self.products.append(product)
        self.total_price += product.price * quantity

    def confirm(self):
        """
        Подтверждает заказ, изменяя его статус на CONFIRMED.
        """
        if self.status != OrderStatus.PENDING:
            raise ValueError(
                "Заказ может быть подтвержден только если он находится в статусе 'ожидание'"
            )
        self.status = OrderStatus.CONFIRMED

    def ship(self):
        """
        Отправляет заказ, изменяя его статус на SHIPPED.
        """
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Заказ может быть отправлен только после подтверждения")
        self.status = OrderStatus.SHIPPED

    def cancel(self):
        """
        Отменяет заказ, изменяя его статус на CANCELLED.
        """
        if self.status in [OrderStatus.SHIPPED, OrderStatus.CANCELLED]:
            raise ValueError("Заказ не может быть отменен")
        self.status = OrderStatus.CANCELLED
        for product in self.products:
            product.quantity += 1
