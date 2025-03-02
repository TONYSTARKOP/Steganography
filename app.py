from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import stepic
import os

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anubhav Steganography Tool")
        self.root.geometry("800x600")

        # Logo
        self.logo = Image.open("logo.png")  
        self.logo = self.logo.resize((100, 50))
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = Label(self.root, image=self.logo)
        self.logo_label.pack(pady=5)

        # Title
        Label(self.root, text="Steganography Tool", font=("Arial", 16, "bold"), bg="blue", fg="white").pack(fill=X)

        # Buttons for Hide/Extract
        self.button_frame = Frame(self.root, bg="gray")
        self.button_frame.pack(fill=X)
        self.hide_button = Button(self.button_frame, text="Hide", font=("Arial", 12, "bold"), bg="red", fg="white", command=self.show_hide_input)
        self.hide_button.pack(side=LEFT, padx=20, pady=10)
        self.extract_button = Button(self.button_frame, text="Extract", font=("Arial", 12, "bold"), bg="red", fg="white", command=self.show_extract_input)
        self.extract_button.pack(side=RIGHT, padx=20, pady=10)

        # Select Image Button
        self.select_image_button = Button(self.root, text="SELECT IMAGE", font=("Arial", 12, "bold"), command=self.load_image)
        self.select_image_button.pack(pady=10)

       
        self.image_label = Label(self.root)
        self.image_label.pack()

        
        self.message_entry = Entry(self.root, font=("Arial", 12))
        self.hide_message_button = Button(self.root, text="Hide", font=("Arial", 12), command=self.hide_message)

        
        self.extracted_entry = Entry(self.root, font=("Arial", 12), show="•")
        self.reveal_button = Button(self.root, text="Reveal", font=("Arial", 12), command=self.reveal_message)
        self.extract_message_button = Button(self.root, text="Extract", font=("Arial", 12), command=self.extract_message)

        self.image = None  
        self.image_path = ""

    def load_image(self):
        """Load JPG or PNG image"""
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return
        
        self.image_path = file_path
        self.image = Image.open(file_path)

        
        if not file_path.lower().endswith(".png"):
            self.image = self.image.convert("RGB")
            self.image_path = file_path.rsplit(".", 1)[0] + ".png"  
            self.image.save(self.image_path)  


        self.image.thumbnail((300, 300))
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.image)

    def show_hide_input(self):
        """Show Hide UI"""
        self.message_entry.pack(pady=5)
        self.hide_message_button.pack(pady=5)

        # Hide Extract UI
        self.extracted_entry.pack_forget()
        self.reveal_button.pack_forget()
        self.extract_message_button.pack_forget()

    def show_extract_input(self):
        """Show Extract UI"""
        self.extracted_entry.pack(pady=5)
        self.reveal_button.pack(pady=5)
        self.extract_message_button.pack(pady=5)

        # Hide Hide UI
        self.message_entry.pack_forget()
        self.hide_message_button.pack_forget()

    def hide_message(self):
        """Hide Message and Allow Custom Save Format"""
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Enter a message to hide.")
            return

        img = Image.open(self.image_path)
        encoded_img = stepic.encode(img, message.encode())

        # Let user choose format (PNG, JPG, JPEG)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("JPG Image", "*.jpg"), ("JPEG Image", "*.jpeg")])
        if not save_path:
            return  # User canceled

        # Convert PNG to user-selected format
        if save_path.lower().endswith(".jpg") or save_path.lower().endswith(".jpeg"):
            encoded_img = encoded_img.convert("RGB")
        
        encoded_img.save(save_path)
        messagebox.showinfo("Success", f"Message hidden successfully! Saved as '{save_path}'")

    def extract_message(self):
        """Extract Hidden Message"""
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        img = Image.open(self.image_path)
        try:
            extracted_message = stepic.decode(img)
            self.extracted_entry.delete(0, END)
            self.extracted_entry.insert(0, extracted_message)
        except:
            messagebox.showerror("Error", "No hidden message found!")

    def reveal_message(self):
        """Toggle Visibility of Extracted Message"""
        if self.extracted_entry.cget("show") == "•":
            self.extracted_entry.config(show="")
        else:
            self.extracted_entry.config(show="•")

if __name__ == "__main__":
    root = Tk()
    app = SteganographyApp(root)
    root.mainloop()
