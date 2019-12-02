from peewee import *
from datetime import datetime
from threading import Timer
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Style


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
        master.title('The Notes App')
        style = ttk.Style(master)
        style.configure('TFrame', bg='#de6262',
                        )
        style.configure('TLabel', font='helvetica 20',
                        foreground='#de6262', anchor='center')
        style.configure('Header.TLabel', font='helvetica 26',
                        foreground='#de6262', anchor='center')
        style.configure('TButton', foreground='#de6262',
                        font='helvetica 20', anchor='center')
        self.current_user = None
        self.length = 0
        # tkinter header
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack(fill=BOTH)
        self.logo = PhotoImage(file='lib/notes-icon.png')
        self.logo = self.logo.subsample(10, 10)
        ttk.Label(self.frame_header, image=self.logo).pack(side=LEFT)
        ttk.Label(self.frame_header, text='The Notes App!', style='Header.TLabel').pack(
            expand=True, fill=BOTH)
        ttk.Label(self.frame_header, wraplength=300,
                  text="Track all your ideas.", style='Header.TLabel').pack(expand=True, fill=BOTH)
        # tkinter main body
        self.frame_body = ttk.Frame(master)
        self.frame_body.pack(expand=True, fill=BOTH)
        self.account_button = ttk.Button(
            self.frame_body, text='Add Account', command=self.sign_up).pack(expand=True, fill=BOTH)
        self.login_button = ttk.Button(
            self.frame_body, text='Login', command=self.login).pack(expand=True, fill=BOTH)
        self.exit_button = ttk.Button(
            self.frame_body, text='Exit', command=self.exit).pack(expand=True, fill=BOTH)
        # tkinter sign up page
        self.frame_sign_up = ttk.Frame(master)
        self.sign_up_label = ttk.Label(
            self.frame_sign_up, text='Sign up below!')
        self.sign_up_label.pack(expand=True, fill=BOTH)
        ttk.Label(self.frame_sign_up, text='First Name:').pack(
            expand=True, fill=BOTH)
        self.entry_first = ttk.Entry(self.frame_sign_up, width=24)
        self.entry_first.pack(expand=True, fill=BOTH)
        ttk.Label(self.frame_sign_up, text='Last Name:').pack(
            expand=True, fill=BOTH)
        self.entry_last = ttk.Entry(self.frame_sign_up, width=24)
        self.entry_last.pack(expand=True, fill=BOTH)
        ttk.Label(self.frame_sign_up, text='Username:').pack(
            expand=True, fill=BOTH)
        self.entry_username = ttk.Entry(self.frame_sign_up, width=24)
        self.entry_username.pack(expand=True, fill=BOTH)
        self.submit_button = ttk.Button(
            self.frame_sign_up, text='Submit', command=self.create_user).pack(expand=True, fill=BOTH)
        # tkinter login page
        self.frame_login = ttk.Frame(master)
        self.login_label = ttk.Label(
            self.frame_login, text='Login below!')
        self.login_label.pack(expand=True, fill=BOTH)
        ttk.Label(self.frame_login, text='Username:').pack(
            expand=True, fill=BOTH)
        self.login_username = ttk.Entry(self.frame_login, width=24)
        self.login_username.pack(expand=True, fill=BOTH)
        self.login_submit = ttk.Button(
            self.frame_login, text='Submit', command=self.submit_on_login).pack(expand=True, fill=BOTH)
        self.back_button = ttk.Button(
            self.frame_login, text='Return to Home', command=self.homepage).pack(expand=True, fill=BOTH)
        # tkinter options page
        self.frame_options = ttk.Frame(master)
        self.options_label = ttk.Label(
            self.frame_options, text='Choose from the following')
        self.options_label.pack(expand=True, fill=BOTH)
        self.submit_button = ttk.Button(
            self.frame_options, text='Add A Note', command=self.show_add_note).pack(expand=True, fill=BOTH)
        self.submit_button = ttk.Button(
            self.frame_options, text='View All Notes', command=self.find_notes_by_user).pack(expand=True, fill=BOTH)
        self.submit_button = ttk.Button(
            self.frame_options, text='Log Out', command=self.homepage).pack(expand=True, fill=BOTH)
        self.submit_button = ttk.Button(
            self.frame_options, text='Delete Your Account', command=self.delete_user).pack(expand=True, fill=BOTH)
        self.submit_button = ttk.Button(
            self.frame_options, text='Exit Program', command=self.exit).pack(expand=True, fill=BOTH)
        # tkinter add notes page
        self.frame_add_note = ttk.Frame(master)
        self.notes_label = ttk.Label(
            self.frame_add_note, text='Add a Note!')
        self.notes_label.pack(expand=True, fill=BOTH)
        ttk.Label(self.frame_add_note, text='Title:').pack(
            expand=True, fill=BOTH)
        self.notes_title = ttk.Entry(self.frame_add_note, width=24)
        self.notes_title.pack(expand=True, fill=BOTH)
        ttk.Label(self.frame_add_note, text='Message:').pack(
            expand=True, fill=BOTH)
        self.notes_body = Text(self.frame_add_note,
                               width=24, font='helvetica 20')
        self.notes_body.pack(expand=True, fill=BOTH)
        self.note_button = ttk.Button(
            self.frame_add_note, text='Submit', command=self.add_note).pack(expand=True, fill=BOTH)
        # tkinter view all notes page
        self.frame_view_notes = ttk.Frame(master)
        self.find_label = ttk.Label(
            self.frame_view_notes, text='Choose a Note!')
        self.find_label.pack(expand=True, fill=BOTH)
        self.choose_label = ttk.Label(self.frame_view_notes,
                                      text='Choose a Note:')
        self.note_number = StringVar()
        self.combobox = ttk.Combobox(
            self.frame_view_notes, textvariable=self.note_number)
        self.choose_button = ttk.Button(self.frame_view_notes, text='Submit')
        # tkinter view single note
        self.frame_chosen_note = ttk.Frame(master)
        self.chosen_note_label = ttk.Label(
            self.frame_chosen_note, text='')
        self.chosen_note_label.pack(expand=True, fill=BOTH)
        self.back_button = ttk.Button(self.frame_chosen_note, text='Return to Options',
                                      command=self.options)
        #  tkinter delete user page
    # initial option list for users to create an account or log in

    def forget_all(self):
        self.frame_chosen_note.pack_forget()
        self.frame_login.pack_forget()
        self.frame_sign_up.pack_forget()
        self.frame_add_note.pack_forget()
        self.frame_view_notes.pack_forget()
        self.frame_options.pack_forget()
        self.frame_body.pack_forget()

    def homepage(self):
        self.forget_all()
        self.frame_body.pack(expand=True, fill=BOTH)

    def sign_up(self):
        self.forget_all()
        self.frame_sign_up.pack(expand=True, fill=BOTH)

    def create_user(self):
        new_user = User(self)
        if new_user.username != None:
            self.current_user = UsersModel(
                first_name=new_user.first_name, last_name=new_user.last_name, username=new_user.username)
            self.current_user.save()
            self.options()

    def login(self):
        self.forget_all()
        self.login_label.config(
            text='Login Below!')
        self.login_username.delete(0, 'end')
        self.frame_login.pack(expand=True, fill=BOTH)

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
        self.forget_all()
        self.frame_options.pack(expand=True, fill=BOTH)
        self.length = len(self.current_user.notes)

    def delete_user(self):
        message_box = messagebox.askyesno(
            'Deletion Warning', 'Are you sure you want to delete your account!', icon='warning')
        if message_box == True:
            self.current_user.delete_instance()
            messagebox.showinfo(
                'User deleted', f'{self.current_user.username} has been deleted.\nGoodbye, {self.current_user.first_name}...FOREVER!')
            self.homepage()

    def show_add_note(self):
        self.notes_label.config(text='Add a Note!')
        self.notes_title.delete(0, 'end')
        self.notes_body.delete(1.0, 'end')
        self.forget_all()
        self.frame_add_note.pack(expand=True, fill=BOTH)

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
        self.choose_label.pack_forget()
        self.combobox.pack_forget()
        self.frame_view_notes.pack(expand=True, fill=BOTH)
        if self.length == 0:
            self.find_label.config(
                text=f'{self.current_user.username} does not have any notes currently.')
            back_button = ttk.Button(self.frame_view_notes, text='Return to Options',
                                     command=self.options).pack(expand=True, fill=BOTH)
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
                          text=f'Note {index+1} - Title: {note.title} - Created: {note.date_created}').pack(expand=True, fill=BOTH)
            # inner_frame = ttk.Frame(self.frame_view_notes).pack(expand=True, fill=BOTH)
            self.choose_label.pack(expand=True, fill=BOTH)
            self.combobox.pack(expand=True, fill=BOTH)
            self.combobox.config(values=note_list)
            self.choose_button.config(command=lambda: self.choose_note(notes))
            self.choose_button.pack(expand=True, fill=BOTH)

    # this function gets the note number generated in find_notes_by_user, finds the corresponding note from the notes_array, and retrieves the note from the database

    def choose_note(self, notes_array):
        self.frame_view_notes.pack_forget()
        self.back_button.pack_forget()
        self.frame_chosen_note.pack(expand=True, fill=BOTH)
        selected = int(self.combobox.get())
        selected_note = NotesModel.get(
            NotesModel.note_id == notes_array[selected-1])
        self.chosen_note_label.config(
            text=f'\tNote {selected }:\n\t\tTitle: {selected_note.title}\n\t\tNote: {selected_note.message}\n\t\tCreated: {selected_note.date_created}\n')
        self.back_button.pack(expand=True, fill=BOTH)

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
    # root.geometry("500x300+450+300")
    root.mainloop()


if __name__ == '__main__':
    main()
