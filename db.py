from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, TextField, DateField, ForeignKeyField

db = MySQLDatabase(
    'db_practice',
    host='localhost',
    user='root',
    password='Zsynth91!'
)


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


if not TGUser.table_exists():
    TGUser.create_table()

if not Note.table_exists():
    Note.create_table()