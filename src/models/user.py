from peewee import CharField

from src.models.entity import Entity


class User(Entity):
    name = CharField()
    password = CharField()
    email = CharField()

    class Meta:
        db_table = "users"
