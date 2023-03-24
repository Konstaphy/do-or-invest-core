from peewee import CharField, IntegerField

from src.models.entity import Entity


class User(Entity):
    name = CharField()
    password = CharField()
    email = CharField()
    penalty = IntegerField()

    class Meta:
        db_table = "users"


class UserTokenData:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
