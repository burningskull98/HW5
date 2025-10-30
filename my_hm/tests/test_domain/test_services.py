"""Тестовый модуль для services"""
from unittest.mock import Mock
import pytest
from my_hm.domain.models import Product, Order, Customer, OrderStatus
from my_hm.domain.services import WarehouseService


@pytest.fixture
def mock_repos():
    product_repo = Mock()
    order_repo = Mock()
    customer_repo = Mock()
    return product_repo, order_repo, customer_repo


def test_create_customer(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    customer_repo.add.return_value = Customer(
        id=1, name="Bradley", email="bradley@gmail.com"
    )

    service = WarehouseService(product_repo, order_repo, customer_repo)
    customer = service.create_customer("Bradley", "bradley@gmail.com")

    assert customer.id == 1
    assert customer.name == "Bradley"
    customer_repo.add.assert_called_once()


def test_create_product(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    product_repo.add.return_value = Product(
        id=1, name="Table", quantity=10, price=1000.0
    )

    service = WarehouseService(product_repo, order_repo, customer_repo)
    product = service.create_product("Table", 10, 1000.0)

    assert product.id == 1
    assert product.name == "Table"
    product_repo.add.assert_called_once()


def test_create_order(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    customer_repo.get.return_value = Customer(id=1, name="Bradley")
    product_repo.get.return_value = Product(id=2, name="Chair", quantity=5, price=20.0)
    order_repo.add.return_value = Order(
        id=3,
        customer_id=1,
        products=[Product(id=2, quantity=4, price=20.0)],
        total_price=20.0,
    )

    service = WarehouseService(product_repo, order_repo, customer_repo)
    order = service.create_order(1, [2])

    assert order.id == 3
    assert order.customer_id == 1
    assert len(order.products) == 1
    customer_repo.get.assert_called_once_with(1)
    product_repo.get.assert_called_once_with(2)
    order_repo.add.assert_called_once()


def test_create_order_customer_not_found(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    customer_repo.get.return_value = None

    service = WarehouseService(product_repo, order_repo, customer_repo)
    with pytest.raises(ValueError, match="Клиент не найден"):
        service.create_order(1, [2])


def test_confirm_order(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    order = Order(
     id=1, status=OrderStatus.PENDING, products=[Product(id=2, quantity=4, price=600.0)]
    )
    order_repo.get.return_value = order

    service = WarehouseService(product_repo, order_repo, customer_repo)
    confirmed = service.confirm_order(1)

    assert confirmed.status == OrderStatus.CONFIRMED
    product_repo.update.assert_called_once()
    order_repo.update.assert_called_once()


def test_confirm_order_not_found(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    order_repo.get.return_value = None

    service = WarehouseService(product_repo, order_repo, customer_repo)
    with pytest.raises(ValueError, match="Заказ не найден"):
        service.confirm_order(1)


def test_ship_order(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    order = Order(id=1, status=OrderStatus.CONFIRMED)
    order_repo.get.return_value = order

    service = WarehouseService(product_repo, order_repo, customer_repo)
    shipped = service.ship_order(1)

    assert shipped.status == OrderStatus.SHIPPED
    order_repo.update.assert_called_once()


def test_cancel_order(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    order = Order(
        id=1, status=OrderStatus.PENDING, products=[Product(id=2, quantity=4, price=900.0)]
    )
    order_repo.get.return_value = order

    service = WarehouseService(product_repo, order_repo, customer_repo)
    cancelled = service.cancel_order(1)

    assert cancelled.status == OrderStatus.CANCELLED
    product_repo.update.assert_called_once()
    order_repo.update.assert_called_once()


def test_get_available_products(mock_repos):
    product_repo, order_repo, customer_repo = mock_repos
    products = [
        Product(id=1, quantity=5,  price=130.0),
        Product(id=2, quantity=0,  price=90.0),
        Product(id=3, quantity=10,  price=210.0),
    ]
    product_repo.list.return_value = products

    service = WarehouseService(product_repo, order_repo, customer_repo)
    available = service.get_available_products()

    assert len(available) == 2
    assert available[0].id == 1
    assert available[1].id == 3
