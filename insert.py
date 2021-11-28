import psycopg2
from datetime import datetime
import time

from dotenv import dotenv_values
from faker import Faker

faker_instance = Faker(['en_US'])


config = dotenv_values(".env")
USER = config.get("USER")
PASSWORD = config.get("PASSWORD")
HOST = config.get("HOST")

def get_data():
    lat, lng, region, country, timezone = faker_instance.location_on_land()
    return dict(
        created_at=f"{datetime.utcnow()}",
        updated_at=f"{datetime.utcnow()}",
        customer_id=faker_instance.uuid4(),
        name=faker_instance.name(),
        region=region,
        country=country,
        lat=lat,
        lng=lng,
        email=faker_instance.ascii_free_email(),
        phone=faker_instance.phone_number()
    )


dsn = (
    "dbname={dbname} "
    "user={user} "
    "password={password} "
    "port={port} "
    "host={host} ".format(
        dbname="orders",
        user=USER,
        password=PASSWORD,
        port=5432,
        host=HOST,
    )
)
print("Started")
conn = psycopg2.connect(dsn)
print("connected")
conn.set_session(autocommit=True)
cur = conn.cursor()
cur.execute(
    """
    create table if not exists customers(
        created_at timestamp,
        updated_at timestamp,
        customer_id uuid PRIMARY KEY,
        name varchar(200),
        region varchar(200),
        country varchar(200),
        lat float,
        lng float,
        email varchar(80),
        phone varchar(30)
    );
    """
)


def get_insert_query():
    return """
        insert into customers values (
          '{created_at}', 
          '{updated_at}', 
          '{customer_id}', 
          '{name}',
          '{region}',
          '{country}',
          {lat},
          {lng},
          '{email}',
          '{phone}'
        )
    """.format(**get_data())


while True:
    query = get_insert_query()
    cur.execute(query)
    print(query)
    time.sleep(0.2)
