from peewee import (
    Model, CharField, IntegerField, TextField, DateField, ForeignKeyField
)
from config import db


class TGUser(Model):
    tg_user_id = IntegerField()
    username = CharField(null=True)

    class Meta:
        database = db


class Note(Model):
    user_id = ForeignKeyField(TGUser, on_delete='CASCADE')
    note = TextField()
    date = DateField()

    class Meta:
        database = db