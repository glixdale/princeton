from Models.Property import Property
from datetime import datetime
import random
from faker import Faker
from database import db
def generate_random_property():
    fake = Faker()

    return Property(
        name=fake.company(),
        date_created=datetime.utcnow(),
        street_number=fake.building_number(),
        street_name=fake.street_name(),
        address_line_2=fake.secondary_address(),
        city=fake.city(),
        zip=fake.zipcode(),
        state=fake.state_abbr(),
        phone=fake.phone_number(),
        phone2=fake.phone_number() if random.choice([True, False]) else None,
        phone3=fake.phone_number() if random.choice([True, False]) else None,
        fax=fake.phone_number() if random.choice([True, False]) else None
    )

# Seed the database with a specified number of random properties
def seed_database(num_properties):
    for _ in range(num_properties):
        random_property = generate_random_property()
        db.session.add(random_property)

    db.session.commit()