import tkinter as tk 
from tkinter import filedialog, messagebox 
from PIL import Image, ImageTk 
from keras.models import load_model 
import numpy as np 
import tensorflow.keras.preprocessing.image as image 
# Load the trained model 
try: 
model = 
load_model("C:/Users/Saiku/Downloads/models.h5/model_inceptionv3t1.h5")  # 
Update the path accordingly 
except Exception as e: 
messagebox.showerror("Error", f"Failed to load model: {str(e)}") 
exit() 
# Define the size of the image 
IMAGE_SIZE = (224, 224) 
image_path = None  # Global variable to store the selected image path 
# Function to load and preprocess the selected image 
def preprocess_image(image_path): 
img = Image.open(image_path) 
img = img.resize(IMAGE_SIZE) 
# Convert grayscale to RGB if image has only one channel 
if img.mode != "RGB":
      img = img.convert("RGB") 
     
    img = image.img_to_array(img) 
    img = np.expand_dims(img, axis=0) 
    img = img / 255.0  # Normalize the pixel values 
    return img 
 
# Function to classify the selected image 
def classify_image(): 
    global image_path 
    if not image_path: 
        messagebox.showwarning("Warning", "Please select an image first.") 
        return 
     
    try: 
        processed_image = preprocess_image(image_path) 
        prediction = model.predict(processed_image) 
        if prediction[0][0] > 0.5: 
            result_label.configure(text="No Kidney Stone Detected", fg="green") 
        else: 
            result_label.configure(text="Kidney Stone Detected", fg="red") 
    except Exception as e: 
        messagebox.showerror("Error", f"Failed to classify image: {str(e)}") 
 
# Function to browse and select an image 
def browse_image(): 
    global image_path 
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image 
files", ".jpg;.jpeg;*.png")]) 
    if image_path: 
        AGE_SIZE=(300,300) 
        img = Image.open(image_path) 
        img = img.resize(AGE_SIZE) 
        img = ImageTk.PhotoImage(img) 
        panel.configure(image=img) 
        panel.image = img

        # Function to clear the displayed image and change button color 
def clear_image(): 
panel.configure(image="") 
result_label.configure(text="", fg="black") 
global image_path 
image_path = None 
# Create the main window 
root = tk.Tk() 
root.geometry("600x400")  # Adjust the window size as needed 
root.title("Kidney Stone Detection") 
root.configure(bg="#f0f0f0")  # Set background color 
# Main heading 
heading_label = tk.Label(root, text="Kideny Stone Detection", font=("Arial", 20, "bold"), 
bg="#f0f0f0") 
heading_label.pack(pady=10) 
# Logo 
logo = Image.open("university-main
logo_96575fd44b35071619e2d5f4abc0b108.webp")  # Replace "ramaiah_logo.png" with 
your logo path 
logo = logo.resize((200,70))  # Adjust the logo size as needed 
logo = ImageTk.PhotoImage(logo) 
logo_label = tk.Label(root, image=logo, bg="#f0f0f0") 
logo_label.pack() 
# Create a panel to display the selected image 
panel = tk.Label(root, bg="#ffffff", borderwidth=2, relief="groove") 
panel.pack(pady=10) 
# Button to browse and select an image 
browse_button = tk.Button(root, text="Browse Image", command=browse_image, 
bg="#4CAF50", fg="white") 
browse_button.pack(pady=10, ipadx=10, ipady=5) 
# Button to classify the selected image

classify_button = tk.Button(root, text="Classify Image", command=classify_image, 
bg="#007bff", fg="white") 
classify_button.pack(pady=10, ipadx=10, ipady=5) 
# Button to clear the displayed image 
clear_button = tk.Button(root, text="Clear Image", command=clear_image, 
bg="#ff6c00", fg="white") 
clear_button.pack(pady=10, ipadx=10, ipady=5) 
# Label to display the classification result 
# Label to display the classification result 
result_label = tk.Label(root, text="", fg="black", font=("Arial", 14)) 
result_label.place(relx=0.5, rely=0.95, anchor="s") 
# Center align the buttons 
browse_button.pack(side=tk.LEFT, padx=200) 
classify_button.pack(side=tk.LEFT, padx=200) 
clear_button.pack(side=tk.LEFT, padx=200) 
# Run the GUI application 
root.mainloop()