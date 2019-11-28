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
        current_user = None

    def login(self):
        try:
            choice = int(input(
                'Enter a number:\n\t(1) - Add an account\n\t(2) - Login\n\t'))
            if choice == 1:
                new_user = User()
                print(f'new user: {new_user}')
                self.current_user = UsersModel(
                    first_name=new_user.first_name, last_name=new_user.last_name, username=new_user.username)
                self.current_user.save()
                self.options()
            elif choice == 2:
                username = input('Enter your username: ')
                self.current_user = self.find_user(username)
                self.options()
            else:
                print('Invalid input')
                self.login()
        except ValueError:
            print('Invalid input')
            self.login()

    def options(self):
        print(self.current_user.username)
        try:
            choice = int(input(
                'Enter a number:\n\t(1) - Add a note\n\t(2) - View all notes\n\t(3) - Log Out\n\t(4) - Exit Program\n\t'))
            if choice == 1:
                print('add_note(current_user)')
            elif choice == 2:
                print('find_notes_by_user(current_user)')
            elif choice == 3:
                self.login()
            elif choice == 4:
                sys.exit()
            else:
                print('Invalid input')
            self.options()
        except ValueError:
            print('Invalid input')
            self.options()

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


class Notes:
    def __init__(self, message):
        self.message = message


home = Home()
home.login()
