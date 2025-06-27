import os
import tkinter as tk
from tkinter import filedialog, simpledialog  # Importing simpledialo

# Function to execute the selected program
def execute_program():
    selected_program = var.get()

    if selected_program == 1:
        os.system("python aviGUI.py")
    elif selected_program == 2:
        hide_data_in_audio()
    elif selected_program == 3:
        recover_data_in_audio()
    elif selected_program == 4:
        os.system("python Encoder.py") 
    elif selected_program == 5:
        os.system("python Decoder.py")
    else:
        os.system("rsa4.py")

# Function to hide data in audio
def hide_data_in_audio():
    print("Starting Program...\n")
    print("=== Hide Data in Audio ===")
    file_text = filedialog.askopenfilename(title="Select Text File to Hide")
    file_audio_old = filedialog.askopenfilename(title="Select Original Audio File (inc. extension)")
    bits_int = simpledialog.askinteger("LSB Bits", "Enter LSB Bits:")  # Use simpledialog.askinteger
    line_string = f"python wav-steg.py -h -d \"{file_text}\" -s \"{file_audio_old}\" -o output\\steg_audio.wav -n {bits_int}"
    os.system(line_string)

# Function to recover data in audio
def recover_data_in_audio():
    print("Starting Program...\n")
    print("=== Recover Data in Audio ===")
    audio_file = filedialog.askopenfilename(title="Select File to Recover From (inc. extension)")
    no_of_lsb_bits = simpledialog.askinteger("LSB Bits", "Enter LSB Bits:")  # Use simpledialog.askinteger
    no_of_bytes = simpledialog.askinteger("Number of Bytes", "Enter Number of Bytes:")
    line_string = f"python wav-steg.py -r -s \"{audio_file}\" -o output\\decoded_audio.txt -n {no_of_lsb_bits} -b {no_of_bytes}"
    os.system(line_string)
    
# GUI setup
window = tk.Tk()
window.title("Steganography Programs")
window.geometry("800x600")  # Set the dimensions to 800x600

var = tk.IntVar()

# Radio buttons for program selection
programs_frame = tk.Frame(window)
programs_frame.pack()

tk.Radiobutton(programs_frame, text="Video Splitter and Combiner", variable=var, value=1).pack(anchor="w")
tk.Radiobutton(programs_frame, text="Hide Data in Audio", variable=var, value=2).pack(anchor="w")
tk.Radiobutton(programs_frame, text="Recover Data in Audio", variable=var, value=3).pack(anchor="w")
tk.Radiobutton(programs_frame, text="Hide Data in Frames", variable=var, value=4).pack(anchor="w")
tk.Radiobutton(programs_frame, text="Recover Data in Frames", variable=var, value=5).pack(anchor="w")
tk.Radiobutton(programs_frame, text="RSA Encrypt/Decrypt", variable=var, value=6).pack(anchor="w")

# Button to execute the selected program
execute_button = tk.Button(window, text="Execute Program", command=execute_program)
execute_button.pack()

window.mainloop()
