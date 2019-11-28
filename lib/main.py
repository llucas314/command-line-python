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


class UsersModel(BaseModel):
    user_id = AutoField()
    first_name = CharField()
    last_name = CharField()
    username = CharField(unique=True)

# defining note model


class NotesModel(BaseModel):
    note_id = AutoField()
    message = TextField()
    date_created = CharField()
    username = ForeignKeyField(UsersModel, field='username', backref='notes')


# establishing tables
db.create_tables([UsersModel])
db.create_tables([NotesModel])


class Home:
    def __init__(self):
        is_logged_in = False
        current_user = None

    def login(self):
        try:
            choice = int(input(
                'Enter a number:\n\t(1) - Add an account\n\t(2) - Login\n\t'))
        except ValueError:
            print('Invalid input')
            self.login()
        if choice == 1:
            new_user = User()
            print(f'new user: {new_user}')
            self.current_user = UsersModel(
                first_name=new_user.first_name, last_name=new_user.last_name, username=new_user.username)
            self.current_user.save()
            print(self.current_user)
        elif choice == 2:
            username = input('Enter your username: ')
            self.current_user = self.find_user(username)
        else:
            print('Invalid input')
            self.login()

    def find_user(self, name):
        try:
            user = UsersModel.get(UsersModel.username == name)
            return user
        except DoesNotExist:
            print('User not found.')
            self.login()


class User:
    def __init__(self):
        self.first_name = input('Enter your first name: ')
        self.last_name = input('Enter your last name: ')
        self.username = self.create_username()

    def create_username(self):
        temp_username = input('Enter a username: ')
        while not self.available(temp_username):
            temp_username = input('Enter a different username: ')
        return temp_username

    def available(self, name):
        existing = UsersModel.select().where(UsersModel.username == name)
        if existing.exists():
            print(f'{name} is already taken by another user.')
            return False
        else:
            return True


home = Home()
home.login()
