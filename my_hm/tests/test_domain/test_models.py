"""Тестовый модуль для models"""

import pytest

from my_hm.domain.models import Product, Order, Customer, OrderStatus


def test_customer_creation():
    customer = Customer(id=1, name="Bradley Pitt", email="bradley@gmail.com")
    assert customer.id == 1
    assert customer.name == "Bradley Pitt"
    assert customer.email == "bradley@gmail.com"


def test_product_creation_valid():
    product = Product(id=1, name="Table", quantity=10, price=1000.0)
    assert product.id == 1
    assert product.name == "Table"
    assert product.quantity == 10
    assert product.price == 1000.0


def test_product_creation_invalid_quantity():
    with pytest.raises(
        ValueError, match="Количество не может быть отрицательным числом"
    ):
        Product(name="Table", quantity=-1, price=1000.0)


def test_product_creation_invalid_price():
    with pytest.raises(ValueError, match="Цена должна быть положительным числом"):
        Product(name="Table", quantity=10, price=0.0)


def test_order_creation():
    order = Order(id=1, customer_id=2, status=OrderStatus.PENDING, total_price=0.0)
    assert order.id == 1
    assert order.customer_id == 2
    assert order.status == OrderStatus.PENDING
    assert order.total_price == 0.0
    assert order.products == []


def test_order_add_product():
    product = Product(id=1, name="Chair", quantity=5, price=20.0)
    order = Order()
    order.add_product(product, quantity=2)
    assert len(order.products) == 1
    assert order.total_price == 40.0
    assert product.quantity == 3


def test_order_add_product_insufficient_stock():
    product = Product(id=1, name="Chair", quantity=1, price=20.0)
    order = Order()
    with pytest.raises(ValueError, match="Недостаточно Chair на складе"):
        order.add_product(product, quantity=2)


def test_order_confirm():
    order = Order(status=OrderStatus.PENDING)
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED


def test_order_confirm_invalid_status():
    order = Order(status=OrderStatus.CONFIRMED)
    with pytest.raises(
        ValueError,
        match="Заказ может быть подтвержден только если он находится в статусе 'ожидание'",
    ):
        order.confirm()


def test_order_ship():
    order = Order(status=OrderStatus.CONFIRMED)
    order.ship()
    assert order.status == OrderStatus.SHIPPED


def test_order_ship_invalid_status():
    order = Order(status=OrderStatus.PENDING)
    with pytest.raises(
        ValueError, match="Заказ может быть отправлен только после подтверждения"
    ):
        order.ship()


def test_order_cancel():
    product = Product(id=1, name="Chair", quantity=3, price=20.0)
    order = Order(status=OrderStatus.PENDING, products=[product])
    order.cancel()
    assert order.status == OrderStatus.CANCELLED
    assert product.quantity == 4


def test_order_cancel_invalid_status():
    order = Order(status=OrderStatus.SHIPPED)
    with pytest.raises(ValueError, match="Заказ не может быть отменен"):
        order.cancel()


def test_order_status_enum():
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.CONFIRMED.value == "confirmed"
    assert OrderStatus.SHIPPED.value == "shipped"
    assert OrderStatus.CANCELLED.value == "cancelled"
