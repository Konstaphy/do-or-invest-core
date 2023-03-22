from peewee import Model, SqliteDatabase, PrimaryKeyField

db = SqliteDatabase("db/database.db")


class Entity(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = "id"
