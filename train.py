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
        def faceAcquisition(self):
            # Path to the base directory containing subdirectories of images
            base_dir = "datasets"

            # Loop through all subdirectories in the base directory
            for subdir, _, files in os.walk(base_dir):
                for filename in files:
                    # Construct the full image path
                    img_path = os.path.join(subdir, filename)
                    
                    # Load the image
                    img = cv2.imread(img_path)
                    
                    # Check if the image was loaded successfully
                    if img is None:
                        print(f"Warning: Could not read image {img_path}. Skipping.")
                        continue

                    try:
                        # Convert the image to grayscale
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                        # Apply Gaussian blur to the image
                        blur = cv2.GaussianBlur(gray, (5, 5), 0)

                        # Apply adaptive thresholding to the image
                        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

                        # Apply morphological operations to the image
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                        dilate = cv2.dilate(thresh, kernel, iterations=3)
                        erode = cv2.erode(dilate, kernel, iterations=3)
                        
                        # You can add further processing here if needed

                    except cv2.error as e:
                        print(f"OpenCV error processing {img_path}: {e}")
                        continue

                # Display the image (optional)
                #cv2.imshow("user_1", erode)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

        messagebox.showinfo("Result", "Acquisition dataset completed!!")

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
                    # Load image using OpenCV
                    img = cv2.imread(image_path)

                    # Validate if image is correctly loaded
                    if img is None:
                        print(f"Skipping {image_path}: Cannot load image.")
                        continue

                    # Convert image to RGB (required by face_recognition)
                    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # Detect faces
                    face_locations = face_recognition.face_locations(rgb_img)
                    encodings = face_recognition.face_encodings(rgb_img, face_locations)

                    if len(encodings) > 0:
                        face_encodings.append(encodings[0])
                        labels.append(label)
                    else:
                        print(f"Warning: No face detected in {image_path}. Skipping.")

                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
                    continue  # Skip the file if any error occurs

        return face_encodings, labels


    def train_classifier(self):
        if not os.path.exists("embeddings"):
            os.makedirs("embeddings")

        face_encodings, labels = self.process_images(self.dataset_path)

        if len(face_encodings) == 0:
            print("Error: No face encodings found. Ensure dataset has images.")
            return

        with open("embeddings/face_encodings.pkl", "wb") as f:
            pickle.dump({"embeddings": face_encodings, "labels": labels}, f)

        print("Embeddings and labels saved successfully.")
        messagebox.showinfo("Result", "Training dataset completed!!")
    

        # Save the embeddings and labels
        with open("embeddings/embeddings.pkl", "wb") as f:
            pickle.dump({"embeddings": face_encodding, "labels": labels}, f)
        # Save embeddings
        with open("embeddings/face_encodings.pkl", "wb") as f:
            pickle.dump(face_encodding, f)

        # Load embeddings
        with open("embeddings/face_encodings.pkl", "rb") as f:
            face_encodding = pickle.load(f)

        print("Embeddings and labels saved successfully.")

        messagebox.showinfo("Result", "Training dataset completed!!")

######################################################################
    def go_to_main(self):
        open_main_window(self.root)       

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()