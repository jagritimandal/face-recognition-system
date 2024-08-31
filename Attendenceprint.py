import tkinter as tk
from tkinter import Label, Button,Frame
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import pandas as pd
from window_manager import open_main_window
#from datetime import datetime

class printAttendence:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        #bg img
        img1=Image.open(r"bg.jpg")
        img1=img1.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        bg_img=Label(self.root,image=self.photoimg1)
        bg_img.place(x=0,y=0,width=1530,height=710)

        #title
        title_lbl=Label(text="Update Attendance ",font=("times new roman",15,"bold"),bg="darkblue",fg="whitesmoke")
        title_lbl.place(x=0,y=1,width=330,height=35)

        frame = Frame(root, width=300, height=850, bg='darkblue')
        frame.place(x=5, y=45)

        # Button for printing attendance
        b1_1 = Button(self.root, text="PRINT ATTENDANCE", command=self.PT, cursor="hand2", font=("times new roman", 10, "bold"), bg="skyblue", fg="black")
        b1_1.place(x=30, y=340, width=200, height=50)

        #back to main button4
        b3_3=Button(text="main page",cursor="hand2",command=self.go_to_main,font=("times new roman",10,"bold"),bg="skyblue",fg="black")
        b3_3.place(x=30,y=450,width=200,height=40)

        frame = Frame(root, width=1000, height=700, bg='darkblue')
        frame.place(x=340, y=35)

    def fix_json_format(filename):
        # Read the content of the JSON file
        with open(filename, 'r') as f:
            json_content = f.read()

        # Attempt to parse the JSON content
        try:
            json_data = json.loads(json_content)
            print("JSON format is valid.")
            return True
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format - {e}")

        # Attempt to fix the JSON format
        try:
            fixed_json_data = json.loads('[' + json_content + ']')
            print("JSON format fixed.")
        except json.JSONDecodeError as e:
            print("Error: Unable to fix JSON format.")
            return False

        # Rewrite the corrected JSON content back to the file
        with open(filename, 'w') as f:
            f.write(json.dumps(fixed_json_data, indent=4))
            print("JSON content rewritten to file.")

        return True
    # Usage example
    filename = 'attendance.json'
    if not fix_json_format(filename):
        print("Unable to fix JSON format.")

    def PT(self):

        try:
            # Load the attendance log from the JSON file
            with open('attendance.json', 'r') as f:
                attendance_log = json.load(f)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in the file.")
            return

        # Convert the attendance log to a Pandas DataFrame
        df = pd.DataFrame(attendance_log)

        # Write the attendance data to an Excel file
        writer = pd.ExcelWriter('attendance_log.xlsx')
        df.to_excel(writer, index=False)
        writer.close()
        messagebox.showinfo("Result", "Attendance log printed to attendance_log.xlsx!")

######################################################################
    def go_to_main(self):
        open_main_window(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    obj = printAttendence(root)
    root.mainloop()