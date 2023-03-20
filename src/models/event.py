from peewee import *

db = SqliteDatabase("db/database.db")


class Entity(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = "id"


class User(Entity):
    name = CharField()

    class Meta:
        db_table = "users"


class Event(Entity):
    title = CharField()
    date = DateTimeField()
    user_id = ForeignKeyField(User)
    is_done = BooleanField()

    class Meta:
        db_table = "events"
