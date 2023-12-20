from rembg import remove
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class PhotoAlteration:
    def __init__(self, root):
        self.root = root
        self.root.title("No Pixel")
        self.root.geometry("500x350")
        self.root.configure(bg='Grey')

        # Configure root to center the main frame
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create the main frame without stretching it to the window's dimensions
        self.main_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        self.main_frame.grid(row=0, column=0)


        # Create ttk style for buttons and frame
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Courier New Baltic", 10), background="#F1C40F")
        self.button_style.configure("TFrame", background="Grey")
        self.button_style.configure("TLabel", background="Grey")
        self.button_style.configure("TCombobox", background="#F1C40F", fieldbackground="#F1C40F")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.photo_button = ttk.Button(self.main_frame, text="Select a Photo (JPEG or PNG format only)", command=self.select_file, style="TButton")
        self.photo_button.grid(row=0, column=0, pady=20, padx=20)

        self.process_button = ttk.Button(self.main_frame, text="Remove Background", command=self.remove_background,
                                         style="TButton")
        self.process_button.grid(row=1, column=0, pady=20, padx=20)

        self.file_label_var = tk.StringVar(self.main_frame)
        self.file_label = ttk.Label(self.main_frame, textvariable=self.file_label_var)
        self.file_label.grid(row=2, column=0, pady=10, padx=20)

        # Label for the file format selection
        self.format_label = ttk.Label(self.main_frame, text="Select Format for Altered Photo", style="TLabel", font=("Courier New Baltic", 12))
        self.format_label.grid(row=3, column=0, pady=(10, 0))  # Adjusting the padding for better spacing

        # Dropdown for file format selection
        self.file_format_var = tk.StringVar()
        self.file_format_dropdown = ttk.Combobox(self.main_frame, textvariable=self.file_format_var,
                                                 values=["JPEG", "PNG"], state="readonly", style="TCombobox")
        self.file_format_dropdown.set("JPEG")  # default value
        self.file_format_dropdown.grid(row=4, column=0,
                                       pady=10)  # This is now row 4 because we've inserted a new widget above

    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=[('Photo Files', ('*.jpg', '*.png'))])
        if filename:
            self.input_path = filename
            self.file_label_var.set(filename.split("/")[-1])
            self.process_button.state(['!disabled'])

    def remove_background(self):
        try:
            with open(self.input_path, 'rb') as i:
                image_data = i.read()
                output_data = remove(image_data)

            selected_format = self.file_format_var.get().lower()
            output_path = filedialog.asksaveasfilename(defaultextension=f".{selected_format}", filetypes=[('PNG Files', '*.png'), ('JPEG Files', '*.jpg')])

            if output_path:
                with open(output_path, 'wb') as o:
                    o.write(output_data)
                messagebox.showinfo("Success", "Background removed and saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing the image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoAlteration(root)
    root.mainloop()
