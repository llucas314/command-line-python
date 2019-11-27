from peewee import *
from datetime import datetime

db = PostgresqlDatabase('notes', user='postgres',
                        password='', host='localhost', post=5432)

db.connect()

# defining base model to establish which db to use


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = AutoField()
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()


class Note(BaseModel):
    note_id = AutoField()
    message = TextField()
    date_created = DateTimeField(formats='%Y-%m-%d %H:%M:%S')
    user_id = ForeignKeyField(User, backref='notes')
