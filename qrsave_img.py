import tkinter as tk
import qrcode
from PIL import Image, ImageTk
from tkinter import filedialog

def generate_qr_code():
    student_name = student_name_entry.get()
    father_name = father_name_entry.get()
    class_name = class_entry.get()

    data = f"Student Name: {student_name}\nFather's Name: {father_name}\nClass: {class_name}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)

    # Add the image to the QR code
    if image_path:
        image = Image.open(image_path)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Resize the image using the PIL 'resize' method
        image = image.resize((50, 50))
        qr_img.paste(image, (100, 100))

        # Prompt the user to save the QR code
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            qr_img.save(save_path)

        qr_img = ImageTk.PhotoImage(qr_img)

        qr_label.config(image=qr_img)
        qr_label.photo = qr_img

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])

# Create the main window
root = tk.Tk()
root.title("QR Code Generator")

# Create and place labels and entry fields for student information
student_name_label = tk.Label(root, text="Student Name:")
student_name_label.pack()
student_name_entry = tk.Entry(root)
student_name_entry.pack()

father_name_label = tk.Label(root, text="Father's Name:")
father_name_label.pack()
father_name_entry = tk.Entry(root)
father_name_entry.pack()

class_label = tk.Label(root, text="Class:")
class_label.pack()
class_entry = tk.Entry(root)
class_entry.pack()

# Add an entry for selecting an image
image_path = None
image_label = tk.Label(root, text="Select an Image:")
image_label.pack()
select_image_button = tk.Button(root, text="Browse", command=select_image)
select_image_button.pack()

generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code)
generate_button.pack()

qr_label = tk.Label(root)
qr_label.pack()

root.mainloop()
