import tkinter as tk
import qrcode
from PIL import Image, ImageTk
from tkinter import filedialog

def generate_qr_code():
    Employee_Name = Employee_Name_entry.get("1.0", "end-1c")  # Get text from the Text widget
    Employee_ID = Employee_ID_entry.get("1.0", "end-1c")
    Sec = class_entry.get("1.0", "end-1c")

    data = f"Employee Name: {Employee_Name}\nEmployee ID: {Employee_ID}\nSec: {Sec}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize the image using the PIL 'resize' method
    qr_img = qr_img.resize((200, 200))

    # Prompt the user to save the QR code
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        qr_img.save(save_path)

    qr_img = ImageTk.PhotoImage(qr_img)

    qr_label.config(image=qr_img)
    qr_label.photo = qr_img

# Create the main window
root = tk.Tk()
root.title("QR Code Generator")

# Create and place labels and entry fields for student information using Text widgets
label_style = {"font": ("Arial", 16, "bold")}
text_style = {"font": ("Arial", 14)}

Employee_Name_label = tk.Label(root, text="Employee Name:", **label_style)
Employee_Name_label.pack()

Employee_Name_entry = tk.Text(root, height=1, width=30, **text_style)
Employee_Name_entry.pack()

Employee_ID_label = tk.Label(root, text="Employee ID:", **label_style)
Employee_ID_label.pack()

Employee_ID_entry = tk.Text(root, height=1, width=30, **text_style)
Employee_ID_entry.pack()

class_label = tk.Label(root, text="Sec:", **label_style)
class_label.pack()

class_entry = tk.Text(root, height=1, width=30, **text_style)
class_entry.pack()

generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code)
generate_button.pack()

qr_label = tk.Label(root)
qr_label.pack()

root.mainloop()
