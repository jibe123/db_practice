from peewee import (
    Model, CharField, IntegerField, TextField, DateField, ForeignKeyField
)
from config import db


class TGUser(Model):
    userid_tg = CharField(unique=True)
    username = CharField(null=True)

    class Meta:
        database = db


class Note(Model):
    userid = ForeignKeyField(TGUser, to_field='userid_tg', on_delete='CASCADE')
    note = TextField()
    date = DateField()

    class Meta:
        database = db