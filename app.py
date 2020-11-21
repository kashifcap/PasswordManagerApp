import tkinter as tk
from database import connection, write_todb, read_todb


class PasswordManager(tk.Frame):
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title('Password Manager')
        self.root.geometry('600x400+250+180')
        self.root.config(bg='blue')

        self.main_frame = tk.Frame(self.root, bg='blue')
        self.main_frame.pack(fill='both')

        self.current_user = ""

        self.login_page()

    def login_page(self):
        self.main_frame.destroy()

        self.root.title("Password Manager - Login")
        self.root.geometry('600x400+250+180')

        self.notification_window = tk.Frame(
            self.root, bg='blue', width=600, height=50)
        self.notification_window.grid(row=0, column=0, pady=10)

        self.main_frame = tk.Frame(self.root, width=570, height=300)
        self.main_frame.grid(row=1, column=0)

        self.login_user_label = tk.Label(self.main_frame, text='Username')
        self.login_user_entrybox = tk.Entry(self.main_frame, width=40)

        self.login_password_label = tk.Label(self.main_frame, text='Password')
        self.login_password_entrybox = tk.Entry(self.main_frame, width=40)

        self.login_button = tk.Button(
            self.main_frame, text='Login', command=self.login)

        self.register_prompt_label = tk.Label(
            self.main_frame, text='New here?')
        self.register_prompt_button = tk.Button(
            self.main_frame, text='Register', command=self.register_page)

        self.login_user_label.place(x=10, y=60)
        self.login_user_entrybox.place(x=200, y=60)
        self.login_password_label.place(x=10, y=120)
        self.login_password_entrybox.place(x=200, y=120)
        self.login_button.place(x=220, y=180)
        self.register_prompt_label.place(x=100, y=240)
        self.register_prompt_button.place(x=400, y=240)

    def register_page(self):
        self.main_frame.destroy()

        self.root.title("Password Manager - Register")
        self.root.geometry("600x500+250+130")

        self.notification_window = tk.Frame(
            self.root, bg='blue', width=600, height=50)
        self.notification_window.grid(row=0, column=0, pady=10)

        self.main_frame = tk.Frame(self.root, width=570, height=400)
        self.main_frame.grid(row=1, column=0)

        self.register_user_label = tk.Label(self.main_frame, text='Username')
        self.register_user_entrybox = tk.Entry(self.main_frame, width=40)

        self.register_email_label = tk.Label(self.main_frame, text='Email')
        self.register_email_entrybox = tk.Entry(self.main_frame, width=40)

        self.register_password_label = tk.Label(
            self.main_frame, text='Password')
        self.register_password_entrybox = tk.Entry(self.main_frame, width=40)

        self.register_confirm_password_label = tk.Label(
            self.main_frame, text='Confirm Password')
        self.register_confirm_password_entrybox = tk.Entry(
            self.main_frame, width=40)

        self.register_button = tk.Button(
            self.main_frame, text='Register', command=self.register)

        self.login_prompt_label = tk.Label(
            self.main_frame, text='Already been here?')
        self.login_prompt_button = tk.Button(
            self.main_frame, text='Login', command=self.login_page)

        self.register_user_label.place(x=10, y=60)
        self.register_user_entrybox.place(x=200, y=60)
        self.register_email_label.place(x=10, y=120)
        self.register_email_entrybox.place(x=200, y=120)
        self.register_password_label.place(x=10, y=180)
        self.register_password_entrybox.place(x=200, y=180)
        self.register_confirm_password_label.place(x=10, y=240)
        self.register_confirm_password_entrybox.place(x=200, y=240)
        self.register_button.place(x=250, y=300)
        self.login_prompt_label.place(x=10, y=360)
        self.login_prompt_button.place(x=200, y=360)

    def login(self):
        user = self.login_user_entrybox.get()
        password = self.login_password_entrybox.get()
        result = read_todb(self.db, user, password)

        if result == "404":
            tk.Label(self.notification_window,
                     text="User doesn't exists!").pack()
        elif result == "401":
            tk.Label(self.notification_window, text="Wrong Password").pack()
        else:
            self.current_user = user
            self.user_window()

    def register(self):
        user = self.register_user_entrybox.get()
        email = self.register_email_entrybox.get()
        password = self.register_password_entrybox.get()
        confirm_password = self.register_confirm_password_entrybox.get()

        if password != confirm_password:
            tk.Label(self.notification_window,
                     text="Password doesn't match!").pack()
        else:
            result = write_todb(self.db, user, password, email)
            if result == "401":
                tk.Label(self.notification_window,
                         text="Username Taken!").pack()
            else:
                self.login_page()

    def user_window(self):
        self.main_frame.destroy()

        self.root.title(f"Password Manager - {self.current_user}")
        self.root.geometry("600x500+250+130")

        self.notification_window = tk.Frame(
            self.root, bg='blue', width=600, height=50)
        self.notification_window.grid(row=0, column=0, pady=10)

        self.add_button = tk.Button(
            self.notification_window, text="Add", command=self.add_cred)
        self.add_button.place(x=50, y=10)

        self.logout_button = tk.Button(
            self.notification_window, text="Logout", command=self.logout)
        self.logout_button.place(x=450, y=10)

    def logout(self):
        self.current_user = ""
        self.login_page()

    def add_cred(self):
        add_cred_window = tk.Toplevel(self.root)
        add_cred_window.config(bg='blue')
        add_cred_window.title("Add Credentials")
        add_cred_window.geometry("500x400+300+100")

        add_cred_frame = tk.Frame(
            add_cred_window, bg='blue', bd=0, width=500, height=400)
        add_cred_frame.grid_propagate(False)

        add_cred_frame.grid(row=0, column=0)

        # Credentials details
        username_label = tk.Label(add_cred_frame, text="Username")
        username_entrybox = tk.Entry(add_cred_frame, width=40)

        email_label = tk.Label(add_cred_frame, text="Email")
        email_entrybox = tk.Entry(add_cred_frame, width=40)

        phnno_label = tk.Label(add_cred_frame, text="Phn no.")
        phnno_entrybox = tk.Entry(add_cred_frame, width=40)

        url_label = tk.Label(add_cred_frame, text="Url")
        url_entrybox = tk.Entry(add_cred_frame, width=40)

        password_label = tk.Label(add_cred_frame, text="Password")
        password_entrybox = tk.Entry(add_cred_frame, width=40)

        username_label.grid(row=0, column=0, padx=20, pady=20)
        username_entrybox.grid(row=0, column=1, padx=20, pady=20)

        email_label.grid(row=1, column=0, padx=20, pady=20)
        email_entrybox.grid(row=1, column=1, padx=20, pady=20)

        phnno_label.grid(row=2, column=0, padx=20, pady=20)
        phnno_entrybox.grid(row=2, column=1, padx=20, pady=20)

        url_label.grid(row=3, column=0, padx=20, pady=20)
        url_entrybox.grid(row=3, column=1, padx=20, pady=20)

        password_label.grid(row=4, column=0, padx=20, pady=20)
        password_entrybox.grid(row=4, column=1, padx=20, pady=20)

        def add_cred_todb():
            add_cred_window.destroy()

        add_button = tk.Button(
            add_cred_frame, text="Add", command=add_cred_todb)
        add_button.grid(row=5, columnspan=2, padx=20, pady=20)


if __name__ == '__main__':
    db = connection()
    root = tk.Tk()
    manager = PasswordManager(root, db)
    root.mainloop()
