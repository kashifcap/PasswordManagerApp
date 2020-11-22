import tkinter as tk
from database import connection, write_todb, read_todb, write_tocreddb, read_tocreddb, delete_tocreddb, update_tocreddb
from functools import partial


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
        self.current_user_password = ""

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

    def edit_cred(self, id, username, email, phone, url, password):
        edit_cred_window = tk.Toplevel(self.root)
        edit_cred_window.config(bg='blue')
        edit_cred_window.title("Edit Credentials")
        edit_cred_window.geometry("500x450+300+100")

        edit_cred_frame = tk.Frame(
            edit_cred_window, bg='blue', bd=0, width=500, height=450)
        edit_cred_frame.grid_propagate(False)

        edit_cred_frame.grid(row=0, column=0)

        # Credentials details
        username_label = tk.Label(edit_cred_frame, text="Username")
        username_entrybox = tk.Entry(edit_cred_frame, width=40)

        email_label = tk.Label(edit_cred_frame, text="Email")
        email_entrybox = tk.Entry(edit_cred_frame, width=40)

        phnno_label = tk.Label(edit_cred_frame, text="Phn no.")
        phnno_entrybox = tk.Entry(edit_cred_frame, width=40)

        url_label = tk.Label(edit_cred_frame, text="Url")
        url_entrybox = tk.Entry(edit_cred_frame, width=40)

        password_label = tk.Label(edit_cred_frame, text="Password")
        password_entrybox = tk.Entry(edit_cred_frame, width=40)

        username_entrybox.insert(0, username)
        email_entrybox.insert(0, email)
        phnno_entrybox.insert(0, phone)
        url_entrybox.insert(0, url)
        password_entrybox.insert(0, password)

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

        def edit_cred_todb():
            new_username = username_entrybox.get()
            new_email = email_entrybox.get()
            new_phone = phnno_entrybox.get()
            new_url = url_entrybox.get()
            new_password = password_entrybox.get()

            update_tocreddb(self.db, id=id, username=new_username,
                            email=new_email, phone=new_phone, url=new_url, password=new_password)

            edit_cred_window.destroy()

            self.user_window()

        edit_button = tk.Button(
            edit_cred_frame, text="Update", command=edit_cred_todb)
        edit_button.grid(row=5, columnspan=2, padx=20, pady=20)

    def delete_cred(self, id):
        delete_tocreddb(self.db, id)
        self.user_window()

    def generate_frame(self):
        frames = []

        results = read_tocreddb(
            db=self.db, user=self.current_user)

        for result in results:
            id = result.get('id')
            username = result.get('username')
            email = result.get('email')
            phone = result.get('phone')
            url = result.get('url')
            password = result.get('password')

            if not username:
                username = "N/A"
            if not email:
                email = "N/A"
            if not phone:
                phone = "N/A"
            if not url:
                url = "N/A"

            frame = tk.Frame(self.scrollable_frame, bg='cyan')

            username_label = tk.Label(frame, text="username")
            username_data_label = tk.Label(frame, text=username)

            email_label = tk.Label(frame, text="email")
            email_data_label = tk.Label(frame, text=email)

            phone_label = tk.Label(frame, text="phone")
            phone_data_label = tk.Label(frame, text=phone)

            url_label = tk.Label(frame, text="url")
            url_data_label = tk.Label(frame, text=url)

            password_label = tk.Label(frame, text="password")
            password_data_label = tk.Label(frame, text=password)

            edit_button = tk.Button(
                frame, text="edit", command=partial(self.edit_cred, id, username, email, phone, url, password))
            delete_button = tk.Button(
                frame, text="delete", command=partial(self.delete_cred, id))

            username_label.grid(row=0, column=0, padx=30)
            username_data_label.grid(row=0, column=1, padx=20)

            email_label.grid(row=1, column=0, padx=30)
            email_data_label.grid(row=1, column=1, padx=20)

            phone_label.grid(row=2, column=0, padx=30)
            phone_data_label.grid(row=2, column=1, padx=20)

            url_label.grid(row=3, column=0, padx=30)
            url_data_label.grid(row=3, column=1, padx=20)

            password_label.grid(row=4, column=0, padx=30)
            password_data_label.grid(row=4, column=1, padx=20)

            edit_button.grid(row=5, column=0, padx=30)
            delete_button.grid(row=5, column=1, padx=20)

            frames.append(frame)

        return frames

    def user_window(self):
        self.main_frame.destroy()

        self.root.title(f"Password Manager - {self.current_user}")
        self.root.geometry("600x500+250+130")

        self.control_window = tk.Frame(
            self.root, bg='blue', width=600, height=50)
        self.control_window.grid_propagate(False)
        self.control_window.grid(row=0, column=0, pady=10)

        self.add_button = tk.Button(
            self.control_window, text="Add", command=self.add_cred)
        self.add_button.grid(row=0, column=0, padx=120,
                             pady=10)  # place(x=50, y=10)

        self.logout_button = tk.Button(
            self.control_window, text="Logout", command=self.logout)
        self.logout_button.grid(row=0, column=1, padx=120,
                                pady=10)  # place(x=450, y=10)

        self.container = tk.Frame(self.root, width=600, height=600, bg='red')
        self.container.grid_propagate(False)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(
            self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor='nw')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        frames = self.generate_frame()

        for i, frame in enumerate(frames):
            frame.grid(row=i, padx=30, pady=10)

        self.container.grid(row=1, columnspan=2, sticky='news')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def logout(self):
        self.current_user = ""
        self.login_page()

    def add_cred(self):
        add_cred_window = tk.Toplevel(self.root)
        add_cred_window.config(bg='blue')
        add_cred_window.title("Add Credentials")
        add_cred_window.geometry("500x450+300+100")

        add_cred_frame = tk.Frame(
            add_cred_window, bg='blue', bd=0, width=500, height=450)
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
            username = username_entrybox.get()
            email = email_entrybox.get()
            phone = phnno_entrybox.get()
            url = url_entrybox.get()
            password = password_entrybox.get()

            if username == "":
                username = None
            if email == "":
                email = None
            if phone == "":
                phone = None
            if url == "":
                url = None
            if password == "":
                label = tk.Label(
                    add_cred_frame, text="*Password field cannot be empty", fg='red', bg='white')
                label.grid(row=6, columnspan=2, pady=5)
            else:
                write_tocreddb(db=self.db, password=password, user=self.current_user,
                               username=username, email=email, phone=phone, url=url)

                add_cred_window.destroy()

                self.user_window()

        add_button = tk.Button(
            add_cred_frame, text="Add", command=add_cred_todb)
        add_button.grid(row=5, columnspan=2, padx=20, pady=20)


if __name__ == '__main__':
    db = connection()
    root = tk.Tk()
    manager = PasswordManager(root, db)
    root.mainloop()
