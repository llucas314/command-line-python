from peewee import *
from datetime import datetime

db = PostgresqlDatabase('notes', user='postgres',
                        password='', host='localhost', port=5432)

db.connect()

# defining base model to establish which db to use


class BaseModel(Model):
    class Meta:
        database = db

# defining user model


class Users(BaseModel):
    user_id = AutoField()
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()

# defining note model


class Notes(BaseModel):
    note_id = AutoField()
    message = TextField()
    date_created = CharField()
    username = ForeignKeyField(Users, field='username', backref='notes')


# establishing tables
db.create_tables([Users])
db.create_tables([Notes])

# create user


def create_user():
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name: ')
    username = input('Enter a username: ')
    while not available(username):
        username = input('Enter a different username: ')
    new_user = Users(username=username, first_name=first_name,
                     last_name=last_name)
    new_user.save()
    return username

# checks if username is available


def available(name):
    existing = Users.select().where(Users.username == name)
    if existing.exists():
        print(f'{name} is already taken by another user.')
        return False
    else:
        return True
# adds notes to current user


# read notes by username


# ren = Users(username='llucas314', first_name='Lorenzo', last_name='Lucas')
# ren.save()
# # ren.delete_instance()
# note = Notes(message='Hi, This is my first note!',
#              date_created=datetime.now().strftime("%a, %b %d, %Y @ %I:%M%p"), username='llucas314')
# note.save()
current_user = create_user()
print(current_user)
