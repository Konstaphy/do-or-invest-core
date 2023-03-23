from peewee import *

from src.models.entity import Entity
from src.models.user import User


class Event(Entity):
    title = CharField()
    date = DateTimeField()
    priority = IntegerField(default=0)
    user_id = ForeignKeyField(User)
    is_done = BooleanField()
    is_expired = BooleanField()

    class Meta:
        db_table = "events"
