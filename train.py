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
        img = Image.open(r"train.jpg")
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

    def train_classifier(self):
        # Ensure embeddings directory exists
        if not os.path.exists("embeddings"):
            os.makedirs("embeddings")

        data_dir = "datasets"

        # Function to process images and extract face embeddings
        def process_images(data_dir):
            embeddings = []
            labels = []

            # Iterate through each student's directory
            for student_id in os.listdir(data_dir):
                student_dir = os.path.join(data_dir, student_id)
                
                if os.path.isdir(student_dir):
                    # Iterate through each image in the student's directory
                    for image_file in os.listdir(student_dir):
                        image_path = os.path.join(student_dir, image_file)
                        print(f"Processing {image_path}")

                        # Load the image
                        image = cv2.imread(image_path)
                        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                        # Find all face locations and their encodings
                        face_locations = face_recognition.face_locations(rgb_image)
                        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

                        for face_encoding in face_encodings:
                            embeddings.append(face_encoding)
                            labels.append(student_id)

            return embeddings, labels

        # Process images and get embeddings and labels
        face_encodding, labels = process_images(data_dir)

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