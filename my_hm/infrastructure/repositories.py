from typing import List, Optional
from sqlalchemy.orm import Session
from my_hm.domain.models import Order, Product, Customer, OrderStatus
from my_hm.domain.repositories import (
    ProductRepository,
    OrderRepository,
    CustomerRepository,
)
from .orm import ProductORM, OrderORM, CustomerORM


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, customer: Customer) -> Customer:
        """
        Добавляет нового клиента в репозиторий и сохраняет его в базе данных.
        """
        customer_orm = CustomerORM(name=customer.name, email=customer.email)
        self.session.add(customer_orm)
        self.session.flush()  # Получить id
        customer.id = customer_orm.id
        return customer

    def get(self, customer_id: int) -> Optional[Customer]:
        """
        Получает клиента по его ID.
        """
        customer_orm = self.session.query(CustomerORM).filter_by(id=customer_id).first()
        if customer_orm:
            return Customer(
                id=customer_orm.id, name=customer_orm.name, email=customer_orm.email
            )
        return None

    def list(self) -> List[Customer]:
        """
        Возвращает список всех клиентов.
        """
        customers_orm = self.session.query(CustomerORM).all()
        return [Customer(id=c.id, name=c.name, email=c.email) for c in customers_orm]

    def update(self, customer: Customer):
        """
        Обновляет информацию о клиенте в базе данных.
        """
        customer_orm = self.session.query(CustomerORM).filter_by(id=customer.id).first()
        if customer_orm:
            customer_orm.name = customer.name
            customer_orm.email = customer.email


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product) -> Product:
        """
        Добавляет новый продукт в репозиторий и сохраняет его в базе данных.
        """
        product_orm = ProductORM(
            name=product.name, quantity=product.quantity, price=product.price
        )
        self.session.add(product_orm)
        self.session.flush()
        product.id = product_orm.id
        return product

    def get(self, product_id: int) -> Optional[Product]:
        """
        Получает продукт по его ID.
        """
        product_orm = self.session.query(ProductORM).filter_by(id=product_id).first()
        if product_orm:
            return Product(
                id=product_orm.id,
                name=product_orm.name,
                quantity=product_orm.quantity,
                price=product_orm.price,
            )
        return None


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order) -> Order:
        """
        Добавляет новый заказ в репозиторий и сохраняет его в базе данных.
        """
        order_orm = OrderORM(
            customer_id=order.customer_id,
            status=order.status.value,
            total_price=order.total_price,
        )
        order_orm.products = [
            self.session.query(ProductORM).filter_by(id=p.id).one()
            for p in order.products
        ]
        self.session.add(order_orm)
        self.session.flush()
        order.id = order_orm.id
        return order

    def get(self, order_id: int) -> Optional[Order]:
        """
        Получает заказ по его ID.
        """
        order_orm = self.session.query(OrderORM).filter_by(id=order_id).first()
        if order_orm:
            products = [
                Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
                for p in order_orm.products
            ]
            return Order(
                id=order_orm.id,
                customer_id=order_orm.customer_id,
                products=products,
                status=OrderStatus(order_orm.status),
                total_price=order_orm.total_price,
            )
        return None

    def list(self) -> List[Order]:
        """
        Возвращает список всех заказов в репозитории.
        """
        orders_orm = self.session.query(OrderORM).all()
        orders = []
        for order_orm in orders_orm:
            products = [
                Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
                for p in order_orm.products
            ]
            orders.append(
                Order(
                    id=order_orm.id,
                    customer_id=order_orm.customer_id,
                    products=products,
                    status=OrderStatus(order_orm.status),
                    total_price=order_orm.total_price,
                )
            )
        return orders

    def update(self, order: Order):
        """
        Обновляет информацию о заказе в базе данных.
        """
        order_orm = self.session.query(OrderORM).filter_by(id=order.id).first()
        if order_orm:
            order_orm.status = order.status.value
            order_orm.total_price = order.total_price
