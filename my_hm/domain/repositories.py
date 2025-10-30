from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Product, Order, Customer


class CustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def list(self) -> List[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer):
        pass


class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def list(self) -> List[Product]:
        pass

    @abstractmethod
    def update(self, product: Product):
        pass


class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def list(self) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order: Order):
        pass
