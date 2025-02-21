from tkinter import Label,Button,Tk,Frame
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2
import face_recognition
import numpy as np
import pickle
from window_manager import open_main_window

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.dataset_path = "datasets"
        self.embeddings_path = "embeddings/face_encodings.pkl"

        
        #bg img
        img1=Image.open(r"bg.png")
        img1=img1.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        bg_img=Label(self.root,image=self.photoimg1)
        bg_img.place(x=0,y=0,width=1530,height=710)

        #title
        title_lbl=Label(text="TRAIN DATA SET ",font=("times new roman",15,"bold"),bg="darkblue",fg="whitesmoke")
        title_lbl.place(x=0,y=1,width=330,height=35)


        frame = Frame(root, width=300, height=850, bg='darkblue')
        frame.place(x=5, y=45)

        # Button for face Acquisition
        b1_1 = Button(self.root, text="Face Acquisition", command=self.faceAcquisition, cursor="hand2",  font=("times new roman", 10, "bold"), bg="skyblue", fg="black")
        b1_1.place(x=30, y=100, width=200, height=50)

        # Button for training data
        b2_2 = Button(self.root, text="TRAIN DATA", command=self.train_classifier, cursor="hand2",  font=("times new roman", 10, "bold"), bg="skyblue", fg="black")
        b2_2.place(x=30, y=250, width=200, height=50)

        #back to main button4
        b3_3=Button(text="main page",cursor="hand2",command=self.go_to_main,font=("times new roman",10,"bold"),bg="skyblue",fg="black")
        b3_3.place(x=30,y=350,width=200,height=40)

        frame = Frame(root, width=1000, height=700, bg='darkblue')
        frame.place(x=340, y=35)

        #first img
        img = Image.open(r"bg.png")
        img = img.resize((600, 400), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=350, y=40, width=600, height=400)

    def faceAcquisition(self):
        face_encodings = []
        labels = []

        # Ensure the embeddings directory exists
        if not os.path.exists("embeddings"):
            os.makedirs("embeddings")

        # Loop through all subdirectories in the dataset
        for person_name in os.listdir(self.dataset_path):
            person_path = os.path.join(self.dataset_path, person_name)

            if not os.path.isdir(person_path):
                continue  # Skip files, only process folders

            label = person_name  # Assuming folder names are student IDs

            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)

                try:
                    # Open image with PIL first to ensure proper format
                    with Image.open(image_path) as img:
                        img = img.convert("RGB")  # Convert to standard RGB
                        img.save(image_path)  # Overwrite corrupted images safely

                    # Reload image using OpenCV
                    img = cv2.imread(image_path)

                    if img is None:
                        print(f"Skipping {image_path}: Cannot load image.")
                        continue

                    # Convert to RGB format
                    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # Detect faces and extract encodings
                    face_locations = face_recognition.face_locations(rgb_img)
                    encodings = face_recognition.face_encodings(rgb_img, face_locations)

                    if encodings:
                        face_encodings.append(encodings[0])
                        labels.append(label)
                        print(f"✔ Face detected in {image_path}")
                    else:
                        print(f"⚠ No face detected in {image_path}. Skipping.")

                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
                    continue  # Skip problematic images

        # Save the extracted encodings
        if face_encodings:
            with open(self.embeddings_path, "wb") as f:
                pickle.dump({"embeddings": face_encodings, "labels": labels}, f)
            print(f"✅ Face encodings saved to {self.embeddings_path}")
            messagebox.showinfo("Result", "Face acquisition completed!!")
        else:
            print("⚠ No face encodings found. Ensure dataset has valid images.")
            messagebox.showwarning("Warning", "No faces detected in dataset!")


    def process_images(self, data_dir):
        face_encodings = []
        labels = []

        for person_name in os.listdir(data_dir):
            person_path = os.path.join(data_dir, person_name)

            if not os.path.isdir(person_path):
                continue  # Skip files, only process folders

            label = person_name  # Assuming folder names are student IDs

            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)

                try:
                    # Open image with PIL first to ensure proper format
                    with Image.open(image_path) as img:
                        img = img.convert("RGB")  # Convert to standard RGB
                        img.save(image_path)  # Overwrite corrupted images safely
                    
                    # Reload image using OpenCV
                    img = cv2.imread(image_path)

                    if img is None:
                        print(f"Skipping {image_path}: Cannot load image.")
                        continue

                    # Convert image to RGB
                    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # Detect faces
                    face_locations = face_recognition.face_locations(rgb_img)
                    encodings = face_recognition.face_encodings(rgb_img, face_locations)

                    if encodings:
                        face_encodings.append(encodings[0])
                        labels.append(label)
                    else:
                        print(f"Warning: No face detected in {image_path}. Skipping.")

                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
                    continue  # Skip problematic images

        return face_encodings, labels

    def train_classifier(self):
        # Load saved encodings
        if not os.path.exists(self.embeddings_path):
            print("⚠ No face encodings found. Run faceAcquisition first.")
            return

        with open(self.embeddings_path, "rb") as f:
            data = pickle.load(f)

        face_encodings, labels = data["embeddings"], data["labels"]

        if not face_encodings:
            print("⚠ No face encodings found. Ensure dataset has images.")
            return

        print("✅ Training completed. Face encodings are ready for recognition.")
        messagebox.showinfo("Result", "Training dataset completed!!")
######################################################################
    def go_to_main(self):
        open_main_window(self.root)       

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()