import customtkinter as ctk
import diec
from CTkMenuBar import CTkMenuBar
from CTkMessagebox import CTkMessagebox
from plyer import notification
import os
import subprocess
import sys
from tkinter import messagebox, filedialog

app = ctk.CTk()
app.geometry("1000x600")
app.title("diec-test-gui")
app.resizable(False, False)

def info_messagebox():
    CTkMessagebox(title="diec-test-gui", message="Package: diec\nPyPi Version: 2.0\nRelease Date: 09.10.2024\nMade by: D&I Projects")

def restart_gui():
    app.destroy()
    python = sys.executable
    script_path = os.path.abspath(__file__)
    subprocess.Popen([python, script_path])

def converting_done():
    notification.notify(
        title="diec-test-gui",
        message="Your text was converted!\nIt's saved in the same directory as the gui.py.\nYou can decode it with our other tool in the tabview!",
        timeout=2
    )

def convert_to_diec():
    input_text = encode_textbox_encode.get("1.0", 'end-1c')
    try:
        diec.encode(input_text)
        converting_done()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during encoding: {e}")

def is_valid_file(selected_file):
    directory = os.path.dirname(selected_file)
    base_name = os.path.basename(selected_file)
    
    if base_name == "encoded.diec":
        counterpart = os.path.join(directory, "key.diec")
    elif base_name == "key.diec":
        counterpart = os.path.join(directory, "encoded.diec")
    else:
        messagebox.showinfo("Invalid file", "Please select a file named 'encoded.diec' or 'key.diec'.")
        return False

    if not os.path.exists(counterpart):
        messagebox.showinfo("Missing counterpart", f"The directory must contain both 'key.diec' and 'encoded.diec'. Missing: {os.path.basename(counterpart)}")
        return False
    return True

def convert_to_text():
    filename = filedialog.askopenfilename(filetypes=[("DIEC files", "*.diec")])
    if not filename:
        messagebox.showinfo("No file selected", "Please select a file.")
        return
    
    if is_valid_file(filename):
        directory = os.path.dirname(filename)
        os.chdir(directory)
        try:
            decoded_text = diec.decode()
            decode_textbox.configure(state="normal")
            decode_textbox.delete("1.0", "end")
            decode_textbox.insert("1.0", decoded_text)
            decode_textbox.configure(state="disabled")
            messagebox.showinfo("Success", "File decoded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decoding: {e}")

menubar = CTkMenuBar(master=app)
menubar.add_cascade("Restart", command=restart_gui)
menubar.add_cascade("Info", command=info_messagebox)

label_title = ctk.CTkLabel(app, text="diec-test-gui", font=("Open Sans", 24))
label_title.pack(pady=5, padx=5)

tabview = ctk.CTkTabview(app)
tabview.pack(padx=20, pady=20)

tabview.add("Encode")
tabview.set("Encode")

encode_label = ctk.CTkLabel(tabview.tab("Encode"), text="Your text:")
encode_label.pack(pady=5, padx=5)

encode_textbox_encode = ctk.CTkTextbox(tabview.tab("Encode"), width=850, height=350)
encode_textbox_encode.pack(pady=5, padx=5)

encode_button = ctk.CTkButton(tabview.tab("Encode"), text="Convert", command=convert_to_diec)
encode_button.pack(padx=5, pady=5)

tabview.add("Decode")

decode_label = ctk.CTkLabel(tabview.tab("Decode"), text="Decoded text:")
decode_label.pack(pady=5, padx=5)

decode_textbox = ctk.CTkTextbox(tabview.tab("Decode"), width=850, height=350)
decode_textbox.pack(pady=5, padx=5)

decode_button = ctk.CTkButton(tabview.tab("Decode"), text="Decode", command=convert_to_text)
decode_button.pack(padx=5, pady=5)

decode_textbox.configure(state="disabled")

app.mainloop()