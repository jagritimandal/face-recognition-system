import cv2
from PIL import Image, ImageTk
import numpy as np
from tkinter import Label,Frame
import face_recognition
import mysql.connector
import tkinter as tk
import json
from datetime import datetime
import pickle
from window_manager import open_main_window
#from json.decoder import JSONDecodeError

class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        #bg img
        img1 = Image.open(r"bg.png")
        img1 = img1.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        bg_img = Label(self.root, image=self.photoimg1)
        bg_img.place(x=0, y=0, width=1530, height=710)

        #title
        title_lbl=tk.Label(text="FACE RECOGNITION ",font=("times new roman",15,"bold"),bg="darkblue",fg="whitesmoke")
        title_lbl.place(x=0,y=1,width=330,height=35)

        frame = Frame(root, width=300, height=850, bg='darkblue')
        frame.place(x=5, y=45)

        b1_1 = tk.Button(self.root, text="Face Recognition", command=self.face_recognize,cursor="hand2", font=("times new roman", 16, "bold"), bg="skyblue", fg="black")
        b1_1.place(x=30, y=320, width=200, height=40)

        #back to main button4
        b3_3=tk.Button(text="main page",cursor="hand2",command=self.go_to_main,font=("times new roman",10,"bold"),bg="skyblue",fg="black")
        b3_3.place(x=30,y=400,width=200,height=40)

        frame = Frame(root, width=1000, height=700, bg='darkblue')
        frame.place(x=340, y=35)

        heading = Label(frame,
                        text='FOR EXITING THE CAMERA Pleace Press "ENTER"',
                        fg='#57a1f8',
                        bg='white',
                        font=("Microsoft Yahei UI Light", 23, 'bold'))
        heading.place(x=30, y=530)


    def mark_attendance(self, student_ids):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password@12345",
            database="face_recognizer"
        )
        my_cursor = conn.cursor()

        # Load existing attendance data from the JSON file
        try:
            with open("attendance.json", "r") as f:
                attendance_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            attendance_data = []

        existing_ids = {entry["Student_id"] for entry in attendance_data if "Student_id" in entry}

        new_attendance_entries = []

        for student_id in student_ids:
            if student_id not in existing_ids:
                my_cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
                result = my_cursor.fetchone()

                if result:
                    dep, classroll, name = result[4], result[0], result[5]
                    new_entry = {
                        "Student_id": student_id,
                        "classroll": classroll,
                        "name": name,
                        "dep": dep,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    new_attendance_entries.append(new_entry)

        attendance_data.extend(new_attendance_entries)

        # Write the updated attendance data back to the JSON file
        with open("attendance.json", "w") as f:
            json.dump(attendance_data, f, indent=4)

        conn.commit()
        conn.close()

    def face_recognize(self):
        # Load embeddings
        with open("embeddings/face_encodings.pkl", "rb") as f:
            embeddings = pickle.load(f)

        video_cap = cv2.VideoCapture(0)

        if not video_cap.isOpened():
            print("Error: Could not open webcam.")
            return

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Error: Could not read frame from webcam.")
                break

            face_locations = face_recognition.face_locations(img)
            face_encodings = face_recognition.face_encodings(img, face_locations)

            recognized_ids = []

            for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                # Convert face encoding to numpy array
                face_encoding = np.array(face_encoding)

                # Use numpy arrays for comparison
                matches = face_recognition.compare_faces(embeddings, face_encoding)
                face_distances = face_recognition.face_distance(embeddings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    student_id = int(best_match_index + 1)  # Ensure student_id is a native Python int
                    recognized_ids.append(student_id)

                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Password@12345",
                        database="face_recognizer"
                    )
                    my_cursor = conn.cursor()
                    my_cursor.execute("SELECT name FROM student WHERE student_id = %s", (student_id,))
                    student_name = my_cursor.fetchone()[0]
                    conn.close()

                    # Draw a box around the face
                    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
                    # Draw a label with the student's name and ID below the face
                    cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f"{student_name} ({student_id})", (left + 6, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

            if recognized_ids:
                self.mark_attendance(recognized_ids)

            cv2.imshow("Welcome To Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()

######################################################################
    def go_to_main(self):
        open_main_window(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    obj = FaceRecognitionSystem(root)
    root.mainloop()


