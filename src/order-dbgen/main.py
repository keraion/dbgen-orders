from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from functools import cached_property
from pprint import pprint
import random
import faker
import factory

faker.Faker.seed(9876)
fake = faker.Faker()


@dataclass
class CustomerAddress:
    id: int
    street_address_line: str
    city: str
    state: str
    zip: str


@dataclass
class Order:
    id: int
    customer: "Customer"
    address: CustomerAddress
    order_date: date
    order_amount_total: float


@dataclass
class Customer:
    id: int
    name: str
    date_of_birth: date
    addresses: list[CustomerAddress] = field(default_factory=list)
    orders: list[Order] = field(default_factory=list)


class CustomerAddressFactory(factory.Factory):
    class Meta:
        model = CustomerAddress

    id = factory.Sequence(lambda n: n)
    street_address_line = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zip = factory.Faker("zipcode")


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    date_of_birth = factory.Faker("date_of_birth")

    @factory.post_generation
    def addresses(self, _create, _extracted, **_kwargs):
        self.addresses = CustomerAddressFactory.build_batch(
            fake.random_int(min=1, max=3)
        )

    @factory.post_generation
    def orders(self, _create, _extracted, **_kwargs):
        self.orders = OrderFactory.build_batch(
            5, customer=self, address=fake.random_element(self.addresses)
        )


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n)
    customer = factory.SubFactory(CustomerFactory)
    address = factory.SubFactory(CustomerAddressFactory)
    order_date = factory.Faker("date_this_month")
    order_amount_total = factory.Faker("pyfloat", right_digits=2)


# print(fake.pyfloat(right_digits=2))
for n in range(5):
    customer = CustomerFactory()
    pprint(customer)

# for n in range(2):
#     order = OrderFactory()
#     print(order)
