import cv2
import qrcode
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import webbrowser  # For opening the HTML file
import time  # For timestamp
import os

# Global variable to store the last scanned QR code and its timestamp
last_scanned_data = ""
last_scan_time = 0

def scan_qr_code_from_camera():
    cap = cv2.VideoCapture(0)  # Open the default camera (camera index 0)
    
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        
        if not ret:
            break
        
        try:
            data, vertices, _ = detector.detectAndDecode(frame)

            if data:
                if is_data_recently_scanned(data):
                    print("QR code already scanned in the last 24 hours. Not saving.")
                else:
                    open_html(data)  # Open HTML with data
                    save_to_excel(data)  # Save data to Excel
                    show_popup(data)
                    break
        except cv2.error as e:
            print("Error detecting QR code:", e)

    cap.release()  # Release the camera
    cv2.destroyAllWindows()

def is_data_recently_scanned(data):
    global last_scan_time, last_scanned_data
    current_time = time.time()
    # Check if the same QR code was scanned within the last 24 hours
    if data == last_scanned_data and current_time - last_scan_time < 24 * 3600:
        return True
    # Update the last scanned data and timestamp
    last_scanned_data = data
    last_scan_time = current_time
    return False

def show_popup(data):
    popup = tk.Tk()
    popup.title("Scanned QR Code")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
   
    # Resize the QR code image using the PIL 'resize' method
    qr_img = qr_img.resize((300, 300), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BILINEAR)

    qr_img = ImageTk.PhotoImage(qr_img)
   
    qr_label = tk.Label(popup, image=qr_img)
    qr_label.photo = qr_img
    qr_label.pack()

    details_label = tk.Label(popup, text="Details: " + data)
    details_label.pack()

    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack()

    popup.mainloop()

def save_to_excel(data):
    try:
        # Check if the Excel file already exists
        if os.path.isfile('qr_data.xlsx'):
            existing_data = pd.read_excel('qr_data.xlsx')
            if data in existing_data['QR Data'].values:
                print("Duplicate data. Not saving.")
                return

        # If the data is not a duplicate, save it to the Excel file
        if not os.path.isfile('qr_data.xlsx'):
            df = pd.DataFrame({'QR Data': [data]})
            df.to_excel('qr_data.xlsx', index=False)
        else:
            updated_data = pd.concat([existing_data, pd.DataFrame({'QR Data': [data]})], ignore_index=True)
            updated_data.to_excel('qr_data.xlsx', index=False)
    except Exception as e:
        print("Error saving data to Excel:", e)

def open_html(data):
    # Create an HTML file with the data and CSS styling
    with open('qr_data.html', 'w') as f:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>QR Code Data</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                }}
                .data-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
                }}
                h1 {{
                    font-size: 24px;
                    color: #333;
                }}
                p {{
                    font-size: 16px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="data-container">
                <h1>QR Code Data</h1>
                <p>{data}</p>
            </div>
        </body>
        </html>
        """
        f.write(html_content)

    # Open the HTML file in a web browser
    webbrowser.open('qr_data.html')

if __name__ == "__main__":
    choice = input("Do you want to scan a QR code from the camera (yes/no)? ").strip().lower()
    if choice == "yes":
        scan_qr_code_from_camera()
    else:
        print("Done.")
