from dataclasses import asdict
from datetime import date, timedelta
import faker
import factory
import polars as pl

from db_data_generator.order.model import (
    Stock,
    Customer,
    CustomerAddress,
    Order,
    OrderLineItem,
)

faker.Faker.seed(9876)
fake = faker.Faker()

ORDER_STATUSES = [
    ["ordered"],
    ["ordered", "cancelled"],
    ["ordered", "processed"],
    ["ordered", "processed", "cancelled"],
    ["ordered", "processed", "shipped"],
    ["ordered", "processed", "shipped", "received"],
    ["ordered", "processed", "shipped", "received", "return_requested"],
    ["ordered", "processed", "shipped", "received", "return_requested", "returned"],
    ["ordered", "processed", "shipped", "received", "closed"],
]


class StockFactory(factory.Factory):
    class Meta:
        model = Stock

    stock_id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(
        lambda s: " ".join(fake.words(fake.random_int(min=1, max=4)))
    )
    quantity = factory.Faker("random_int", min=0, max=150)
    price_per_item = factory.Faker(
        "pyfloat",
        right_digits=2,
        left_digits=fake.random_int(min=1, max=4),
        positive=True,
    )


class CustomerAddressFactory(factory.Factory):
    class Meta:
        model = CustomerAddress

    address_id = factory.Sequence(lambda n: n)
    street_address_line = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zip = factory.LazyAttribute(
        lambda addr: fake.zipcode_in_state(state_abbr=addr.state)
    )


def generate_order_status_dates(start_date: date, order_status_list: list[str]):
    output_dates = [start_date]
    for _ in range(len(order_status_list) - 1):
        output_dates.append(output_dates[-1] + timedelta(fake.random_int(0, 5)))
    return output_dates


def generate_order_status_id(order_status_list: list[str]):
    return [i for i, _ in enumerate(order_status_list)]


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    order_id = factory.Sequence(lambda n: n)
    order_status = factory.Faker("random_element", elements=ORDER_STATUSES)
    order_status_id = factory.LazyAttribute(
        lambda s: generate_order_status_id(s.order_status)
    )
    status_date = factory.LazyAttribute(
        lambda s: generate_order_status_dates(
            fake.past_date(start_date=date(2024, 1, 1)), s.order_status
        )
    )

    @factory.post_generation
    def order_lines(self, _create, _extracted, **_kwargs):
        self.order_lines = OrderLineItemFactory.build_batch(
            fake.random_int(1, 15),
            order=self.order_id,
        )


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer

    customer_id = factory.Sequence(lambda n: n)
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
            fake.random_int(0, 50),
            customer=self.customer_id,
            address=fake.random_element(self.addresses).address_id,
        )


def generate_from_factory(number_of_items, factory):
    return [factory() for _ in range(number_of_items)]


ALL_STOCK = generate_from_factory(200, StockFactory)


class OrderLineItemFactory(factory.Factory):
    class Meta:
        model = OrderLineItem

    order_line_id = factory.Sequence(lambda n: n)
    order = None
    stock = factory.Faker("random_element", elements=ALL_STOCK)
    quantity_ordered = factory.Faker("random_int", min=1, max=10)


def generate_dataframe(number_of_items: int, factory: factory.Factory):
    df = pl.DataFrame(data=map(asdict, generate_from_factory(number_of_items, factory)))
    print(df)
    return df
