from peewee import *
from datetime import datetime
import sys

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
    return new_user

# checks if username is available


def available(name):
    existing = Users.select().where(Users.username == name)
    if existing.exists():
        print(f'{name} is already taken by another user.')
        return False
    else:
        return True

# adds notes to current user


def add_note(user):
    message = input('Write a note: ')
    new_note = Notes(message=message, date_created=datetime.now().strftime(
        "%a, %b %d, %Y @ %I:%M%p"), username=user.username)
    new_note.save()
    return new_note

# read notes by username


def find_notes_by_user(user):
    print(f'Notes by {user.username}')
    for index, note in enumerate(user.notes, start=1):
        print(
            f'\tNote {index}: {note.message}\n\tCreated: {note.date_created}')
# finds user


def find_user(name):
    user = Users.select().where(Users.username == name)
    if user.exists():
        return user
    else:
        print('User not found.')
        start()

# creates user or logs in


def login():
    try:
        choice = int(input(
            'Enter a number:\n\t(1) - Add an account\n\t(2) - Login\n\t'))
    except ValueError:
        print('Invalid input')
        start()
    if choice == 1:
        current_user = create_user()
        return current_user
    elif choice == 2:
        username = input('Enter your username: ')
        current_user = find_user(username)
        return current_user
    else:
        print('Invalid input')
        start()

# select options for logged in user


def options(current_user):
    try:
        choice = int(input(
            'Enter a number:\n\t(1) - Add a note\n\t(2) - View all notes\n\t(3) - Log Out\n\t(4) - Exit Program'))
    except ValueError:
        print('Invalid input')
        options(current_user)
    if choice == 1:
        add_note(current_user)

    elif choice == 2:
        find_notes_by_user(current_user)

    elif choice == 3:
        start()
    elif choice == 4:
        sys.exit()
    else:
        print('Invalid input')
        options(current_user)

# starts app


def start():
    current_user = login()
    options(current_user)


start()
