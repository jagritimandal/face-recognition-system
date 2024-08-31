import tkinter as tk

def open_main_window(current_window):
    from main import Face_Recognition_System
    current_window.destroy()
    new_window = tk.Tk()
    app = Face_Recognition_System(new_window)
    new_window.mainloop()

def open_student_window(current_window):
    from student import Student
    current_window.destroy()
    new_window = tk.Tk()
    app = Student(new_window)
    new_window.mainloop()

def open_train_window(current_window):
    from train import Train
    current_window.destroy()
    new_window = tk.Tk()
    app = Train(new_window)
    new_window.mainloop()

def open_face_window(current_window):
    from facerecognition import FaceRecognitionSystem
    current_window.destroy()
    new_window = tk.Tk()
    app = FaceRecognitionSystem(new_window)
    new_window.mainloop()

def open_update_window(current_window):
    from Attendenceprint import printAttendence
    current_window.destroy()
    new_window = tk.Tk()
    app = printAttendence(new_window)
    new_window.mainloop()

