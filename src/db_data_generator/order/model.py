from dataclasses import dataclass, field
from datetime import date


@dataclass
class Stock:
    stock_id: int
    name: str
    quantity: int
    price_per_item: float


@dataclass
class CustomerAddress:
    address_id: int
    street_address_line: str
    city: str
    state: str
    zip: str


@dataclass
class OrderStatus:
    order_status_id: int
    status: str
    status_date: date


@dataclass
class OrderLineItem:
    order_line_id: int
    order: "Order"
    quantity_ordered: int
    stock: list[Stock] = field(default_factory=list)


@dataclass
class Order:
    order_id: int
    customer: int
    address: int
    order_status_id: list[int] = field(default_factory=list)
    status_date: list[date] = field(default_factory=list)
    order_status: list[OrderStatus] = field(default_factory=list)
    order_lines: list[OrderLineItem] = field(default_factory=list)


@dataclass
class Customer:
    customer_id: int
    name: str
    date_of_birth: date
    addresses: list[CustomerAddress] = field(default_factory=list)
    orders: list[Order] = field(default_factory=list)
