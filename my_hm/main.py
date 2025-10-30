from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_hm.domain.services import WarehouseService
from my_hm.infrastructure.orm import Base
from my_hm.infrastructure.repositories import (
    SqlAlchemyProductRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyCustomerRepository,
)
from my_hm.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from my_hm.infrastructure.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)
    customer_repo = SqlAlchemyCustomerRepository(session)
    uow = SqlAlchemyUnitOfWork(session)
    warehouse_service = WarehouseService(product_repo, order_repo, customer_repo)

    with uow:
        """Создание клиента"""
        customer = warehouse_service.create_customer(
            name="Bradley Pitt", email="bradley@gmail.com"
        )
        print(f"Created customer: {customer}")

        """ Создание товаров"""
        product1 = warehouse_service.create_product(
            name="Table", quantity=10, price=1000.0
        )
        product2 = warehouse_service.create_product(
            name="Chair", quantity=50, price=20.0
        )
        print(f"Created products: {product1}, {product2}")

        """ Создание заказа"""
        order = warehouse_service.create_order(
            customer_id=customer.id, product_ids=[product1.id, product2.id]
        )
        print(f"Created order: {order}")

        """Подтверждение заказа"""
        confirmed_order = warehouse_service.confirm_order(order.id)
        print(f"Confirmed order: {confirmed_order}")

        """Отгрузка заказа"""
        shipped_order = warehouse_service.ship_order(order.id)
        print(f"Shipped order: {shipped_order}")

        uow.commit()
    if __name__ == "__main__":
        main()
