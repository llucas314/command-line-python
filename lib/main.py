from peewee import *
from datetime import datetime

import sys
from tkinter import *
from tkinter import ttk


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
    title = CharField()
    message = TextField()
    date_created = CharField()
    username = ForeignKeyField(
        UsersModel, field='username', backref='notes', on_delete='CASCADE')


# establishing tables
db.create_tables([UsersModel])
db.create_tables([NotesModel])


class Home:
    def __init__(self, master):
        self.current_user = None
        self.length = 0
        # tkinter header
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        self.logo = PhotoImage(file='lib/notes-icon.png')
        self.logo = self.logo.subsample(25, 25)
        ttk.Label(self.frame_header, image=self.logo).grid(
            row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text='The Notes App!').grid(
            row=0, column=1)
        ttk.Label(self.frame_header, wraplength=300,
                  text="Create and view all your ideas.").grid(row=1, column=1)
        # tkinter main body
        self.frame_body = ttk.Frame(master)
        self.frame_body.pack()
        self.account_button = ttk.Button(
            self.frame_body, text='Add Account', command=self.sign_up).grid(row=0, column=0)
        self.login_button = ttk.Button(
            self.frame_body, text='Login').grid(row=0, column=1)
        self.exit_button = ttk.Button(
            self.frame_body, text='Exit', command=self.exit).grid(row=1, columnspan=2)
        # tkinter login page
        self.frame_sign_up = ttk.Frame(master)
        self.sign_up_label = ttk.Label(
            self.frame_sign_up, text='Sign up below!')
        self.sign_up_label.pack()
        ttk.Label(self.frame_sign_up, text='First Name:').pack()
        self.entry_first = ttk.Entry(self.frame_sign_up, width=24)
        self.entry_first.pack()
        ttk.Label(self.frame_sign_up, text='Last Name:').pack()
        self.entry_last = ttk.Entry(self.frame_sign_up, width=24)
        self.entry_last.pack()
        ttk.Label(self.frame_sign_up, text='Username:').pack()
        self.entry_username = ttk.Entry(self.frame_sign_up, width=24)
        self.entry_username.pack()
        self.submit_button = ttk.Button(
            self.frame_sign_up, text='Submit', command=self.create_user).pack()

    # initial option list for users to create an account or log in

    def sign_up(self):
        self.frame_body.pack_forget()
        self.frame_sign_up.pack()

    def create_user(self):
        new_user = User(self)
        if new_user.username != None:
            self.current_user = UsersModel(
                first_name=new_user.first_name, last_name=new_user.last_name, username=new_user.username)
            self.current_user.save()
            self.options()

    def exit(self):
        sys.exit()
    # def login(self, choice):
    #     if choice == 1:
    #         new_user = User()
    #         self.current_user = UsersModel(
    #             first_name=new_user.first_name, last_name=new_user.last_name, username=new_user.username)
    #         self.current_user.save()
    #         self.options()
    #     elif choice == 2:
    #         username = input('Enter your username: ')
    #         self.current_user = self.find_user(username)
    #         self.options()
    #     elif choice == 3:
    #         sys.exit()
    #     else:
    #         print('Invalid input')
    #         self.login()

    # options for creating and viewing notes or deleting account

    def options(self):
        self.length = len(self.current_user.notes)
        try:
            choice = int(input(
                f'Hello, {self.current_user.first_name}! Choose an option:\n\t(1) - Add a note\n\t(2) - View all notes\n\t(3) - Log Out\n\t(4) - Delete Your Account\n\t(5) - Exit Program\n\t'))
            if choice == 1:
                self.add_note()
            elif choice == 2:
                self.find_notes_by_user()
            elif choice == 3:
                self.login()
            elif choice == 4:
                self.delete_user()
            elif choice == 5:
                sys.exit()
            else:
                print('Invalid input')
            self.options()
        except ValueError:
            print('Invalid input')
            self.options()

    def delete_user(self):
        answer = input('Are you sure? (y/n):\n').lower()
        if answer == 'y' or answer == 'yes':
            print(
                f'{self.current_user.username} has been deleted.\nGoodbye, {self.current_user.first_name}...FOREVER!')
            self.current_user.delete_instance()
            self.login()
        elif answer == 'n' or answer == 'no':
            self.options()
        else:
            print('Invalid Input')

    def add_note(self):
        title = input('Enter a title for your note: ')
        message = input('Write the body of your note: ')
        new_note = Note(title, message, self.current_user.username)
        new_note.create_note()
        self.length = len(self.current_user.notes)
        print('Note created.')

    def find_notes_by_user(self):
        if self.length == 0:
            print(f'{self.current_user.username} does not have any notes currently.')
        else:
            print(f'Notes by {self.current_user.username}:')
            # the notes are printed in decsending order and their id is saved in an array to use to retrieve the message later
            notes = []
            for index, note in enumerate(self.current_user.notes):
                notes.append({note.note_id})
                print(
                    f'\tNote {self.length-index} - Title: {note.title} - Created: {note.date_created}\n')
            self.choose_note(notes)

    # this function gets the note number generated in find_notes_by_user, finds the corresponding note from the notes_array, and retrieves the note from the database
    def choose_note(self, notes_array):
        try:
            selected = self.length-int(input('Select a note by its number: '))
            if selected >= 0 and selected < self.length:
                selected_note = NotesModel.get(
                    NotesModel.note_id == notes_array[selected])
                print(
                    f'\tNote {selected + self.length}:\n\t\tTitle: {selected_note.title}\n\t\tNote: {selected_note.message}\n\t\tCreated: {selected_note.date_created}\n')
            else:
                print('Invalid Input')
                self.choose_note(notes_array)
        except ValueError:
            print('Invalid input')
            self.choose_note(notes_array)

    def find_user(self, name):
        try:
            user = UsersModel.get(UsersModel.username == name)
            return user
        except DoesNotExist:
            print(f'User: {name} not found.')
            self.login()


class User:
    def __init__(self, user_input):
        self.first_name = user_input.entry_first.get()
        self.last_name = user_input.entry_last.get()
        self.username = self.create_username(user_input)

    def create_username(self, user_input):
        temp_username = user_input.entry_username.get()
        if self.available(temp_username, user_input):
            user_input.sign_up_label.config(text="User Created")
            return temp_username
        else:
            temp_username = None
            return temp_username

    def available(self, name, user_input):
        existing = UsersModel.select().where(UsersModel.username == name)
        if existing.exists():
            user_input.sign_up_label. config(
                text=f'{name} is already taken by another user.')
            # user_input.sign_up_label.set(
            #     f'{name} is already taken by another user.')
            # print(f'{name} is already taken by another user.')
            return False
        else:
            return True


class Note:
    def __init__(self, title, message, user):
        self.title = title
        self.message = message
        self.username = user

    def create_note(self):
        new_note = NotesModel(title=self.title, message=self.message, date_created=datetime.now().strftime(
            "%a, %b %d, %Y @ %I:%M%p"), username=self.username)
        new_note.save()


# home = Home()
# home.login()
def main():
    root = Tk()
    home = Home(root)
    root.mainloop()


if __name__ == '__main__':
    main()
