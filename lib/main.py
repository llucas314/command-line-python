from peewee import *
from datetime import datetime
from threading import Timer
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
            self.frame_body, text='Login', command=self.login).grid(row=0, column=1)
        self.exit_button = ttk.Button(
            self.frame_body, text='Exit', command=self.exit).grid(row=1, columnspan=2)
        # tkinter sign up page
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
        # tkinter login page
        self.frame_login = ttk.Frame(master)
        self.login_label = ttk.Label(
            self.frame_login, text='Login below!')
        self.login_label.pack()
        ttk.Label(self.frame_login, text='Username:').pack()
        self.login_username = ttk.Entry(self.frame_login, width=24)
        self.login_username.pack()
        self.login_submit = ttk.Button(
            self.frame_login, text='Submit', command=self.submit_on_login).pack()
        # tkinter options page
        self.frame_options = ttk.Frame(master)
        self.options_label = ttk.Label(
            self.frame_sign_up, text='Choose from the following')
        self.options_label.pack()
        self.submit_button = ttk.Button(
            self.frame_options, text='Add A Note', command=self.show_add_note).pack()
        self.submit_button = ttk.Button(
            self.frame_options, text='View All Notes', command=self.find_notes_by_user).pack()
        self.submit_button = ttk.Button(
            self.frame_options, text='Log Out').pack()
        self.submit_button = ttk.Button(
            self.frame_options, text='Delete Your Account', command=self.delete_user).pack()
        self.submit_button = ttk.Button(
            self.frame_options, text='Exit Program', command=self.exit).pack()
        # tkinter add notes page
        self.frame_add_note = ttk.Frame(master)
        self.notes_label = ttk.Label(
            self.frame_add_note, text='Add a Note!')
        self.notes_label.pack()
        ttk.Label(self.frame_add_note, text='Title:').pack()
        self.notes_title = ttk.Entry(self.frame_add_note, width=24)
        self.notes_title.pack()
        ttk.Label(self.frame_add_note, text='Message:').pack()
        self.notes_body = Text(self.frame_add_note, width=24)
        self.notes_body.pack()
        self.note_button = ttk.Button(
            self.frame_add_note, text='Submit', command=self.add_note).pack()
        # tkinter view all notes page
        self.frame_view_notes = ttk.Frame(master)
        self.find_label = ttk.Label(
            self.frame_view_notes, text='Choose a Note!')
        self.find_label.pack()
        # view single note
        self.frame_chosen_note = ttk.Frame(master)
        self.chosen_note_label = ttk.Label(
            self.frame_chosen_note, text='')
        self.chosen_note_label.pack()
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

    def login(self):
        self.frame_body.pack_forget()
        self.frame_login.pack()

    def submit_on_login(self):
        self.current_user = self.find_user(self.login_username.get())
        if self.current_user.first_name:
            self.login_label.config(
                text=f'Welcome back, {self.current_user.first_name}!')
        self.options()

    def exit(self):
        sys.exit()

    # options for creating and viewing notes or deleting account

    def options(self):
        self.frame_login.pack_forget()
        self.frame_sign_up.pack_forget()
        self.frame_add_note.pack_forget()
        self.frame_options.pack()
        self.length = len(self.current_user.notes)

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

    def show_add_note(self):
        self.notes_label.config(text='Add a Note!')
        self.notes_title.delete(0, 'end')
        self.notes_body.delete(1.0, 'end')
        self.frame_options.pack_forget()
        self.frame_add_note.pack()

    def add_note(self):
        title = self.notes_title.get()
        message = self.notes_body.get(1.0, 'end')
        new_note = Note(title, message, self.current_user.username)
        new_note.create_note()
        self.length = len(self.current_user.notes)
        self.notes_label.config(text='Note created.')
        timer = Timer(1.0, self.options)
        timer.start()

    def find_notes_by_user(self):
        self.frame_options.pack_forget()
        self.frame_view_notes.pack()
        if self.length == 0:
            self.find_label.config(
                text=f'{self.current_user.username} does not have any notes currently.')
        else:
            self.find_label.config(
                text=f'Notes by {self.current_user.username}:')
            # the notes are printed in decsending order and their id is saved in an array to use to retrieve the message later
            notes = []
            note_list = []
            for index, note in enumerate(self.current_user.notes):
                notes.append({note.note_id})
                note_list.append(index+1)
                ttk.Label(self.frame_view_notes,
                          text=f'Note {index+1} - Title: {note.title} - Created: {note.date_created}').pack()
            # inner_frame = ttk.Frame(self.frame_view_notes).pack()
            ttk.Label(self.frame_view_notes,
                      text='Choose a Note:').pack(side=LEFT)
            note_number = StringVar()
            combobox = ttk.Combobox(
                self.frame_view_notes, textvariable=note_number)
            combobox.pack()
            combobox.config(values=note_list)
            choose_button = ttk.Button(self.frame_view_notes, text='Submit',
                                       command=lambda: self.choose_note(notes, combobox)).pack(side=RIGHT)

    # this function gets the note number generated in find_notes_by_user, finds the corresponding note from the notes_array, and retrieves the note from the database

    def choose_note(self, notes_array, box):
        self.frame_view_notes.pack_forget()
        self.frame_chosen_note.pack()
        selected = int(box.get())
        selected_note = NotesModel.get(
            NotesModel.note_id == notes_array[selected-1])
        self.chosen_note_label.config(
            text=f'\tNote {selected }:\n\t\tTitle: {selected_note.title}\n\t\tNote: {selected_note.message}\n\t\tCreated: {selected_note.date_created}\n')
        print(f'\tNote {selected }:\n\t\tTitle: {selected_note.title}\n\t\tNote: {selected_note.message}\n\t\tCreated: {selected_note.date_created}\n')
        print(notes_array)

    def find_user(self, name):
        try:
            user = UsersModel.get(UsersModel.username == name)
            return user
        except DoesNotExist:
            self.login_label.config(text=f'User: {name} not found.')
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
