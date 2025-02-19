from tkinter import Label,Button,Tk,Frame,Entry,END,Toplevel
from tkinter import messagebox
from main import Face_Recognition_System
from PIL import Image, ImageTk


class login:

    def __init__(self, root):
        self.root = root
        root.title('LOGIN')
        self.root.geometry("1230x690+0+0")
        self.root.configure(bg='white')
        self.root.resizable(False, False)

        def signin():
            username = user.get()
            password = code.get()

            if username == 'admin' and password == '1234':
                # Destroy the login window
                root.destroy()
                # Create the main application window
                main_root = Tk()
                main_root.title("Main Application")
                main_root.geometry("800x600")
                # Instantiate your main application class (Face_Recognition_System)
                app = Face_Recognition_System(main_root)
                # Start the main event loop
                main_root.mainloop()
            else:
                # Handle incorrect username/password
                messagebox.showerror("Error", "Incorrect username or password")

        #bg img
        img1=Image.open(r"bg.png")
        img1=img1.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        bg_img=Label(self.root,image=self.photoimg1)
        bg_img.place(x=0,y=0,width=1530,height=710)

        frame = Frame(root, width=300, height=350, bg='darkblue')
        frame.place(x=435, y=70)

        #first img
        img = Image.open(r"bg.png")
        img = img.resize((70, 70), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=550, y=30, width=70, height=70)

        heading = Label(frame,
                        text='sign in',
                        fg='#57a1f8',
                        bg='white',
                        font=("Microsoft Yahei UI Light", 23, 'bold'))
        heading.place(x=100, y=30)

        def on_enter_username(e):
            user.delete(0, END)

        def on_leave_username(e):
            name = user.get()
            if name == '':
                user.insert(0, "username")

        user = Entry(frame,
                     width=25,
                     fg='black',
                     border=0,
                     bg='white',
                     font=("Microsoft Yahei UI Light", 11))
        user.place(x=30, y=80)
        user.insert(0, 'username')
        user.bind('<FocusIn>', on_enter_username)
        user.bind('<FocusOut>', on_leave_username)

        def on_enter_password(e):
            code.delete(0, END)

        def on_leave_password(e):
            name = code.get()
            if name == '':
                code.insert(0, "password")

        code = Entry(frame,
                     width=25,
                     fg='black',
                     border=0,
                     bg='white',
                     font=("Microsoft Yahei UI Light", 11))
        code.place(x=30, y=150)
        code.insert(0, 'password')
        code.bind('<FocusIn>', on_enter_password)
        code.bind('<FocusOut>', on_leave_password)

        Frame(frame, width=255, height=2, bg='black').place(x=25, y=177)

        Button(frame,
               width=20,
               pady=7,
               text='Sign in',
               fg='black',
               bg='skyblue',
               border=0,
               command=signin).place(x=50, y=204)
        label = Label(frame,
                      text="Don't have an account",
                      fg='black',
                      bg='white',
                      font=("Microsoft Yahei UI Light", 9))
        label.place(x=55, y=270)

        sign_up = Button(frame,
                         width=10,
                         text='Sign in',
                         fg='black',
                         bg='skyblue',
                         border=0,
                         cursor='hand2')
        sign_up.place(x=200, y=270)

        #==================function=================

    def main(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition_System(self.new_window)


if __name__ == "__main__":
    root = Tk()
    obj = login(root)
    root.mainloop()
