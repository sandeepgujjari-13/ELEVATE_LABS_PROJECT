from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from tkinter import filedialog, messagebox
import tkinter as tk

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_key_to_file(key, filename):
    key_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as key_file:
        key_file.write(key_bytes)

def load_key_from_file(filename, is_private=True):
    with open(filename, 'rb') as key_file:
        key_data = key_file.read()
        if is_private:
            key = serialization.load_pem_private_key(key_data, password=None, backend=default_backend())
        else:
            key = serialization.load_pem_public_key(key_data, backend=default_backend())
        return key

def encrypt_file(public_key, input_file_path, output_file_path):
    with open(input_file_path, 'rb') as file:
        plaintext = file.read()

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file_path, 'wb') as file:
        file.write(ciphertext)

def decrypt_file(private_key, input_file_path, output_file_path):
    with open(input_file_path, 'rb') as file:
        ciphertext = file.read()

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file_path, 'wb') as file:
        file.write(plaintext)

def browse_file(entry_widget):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def browse_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, folder_path)

def encrypt_button_click():
    try:
        input_file_path = entry_input_file.get()
        output_folder_path = entry_output_folder.get()

        public_key = load_key_from_file('public_key.pem', is_private=False)
        encrypt_file(public_key, input_file_path, output_folder_path + "/encrypted_file")
        messagebox.showinfo("Success", "Encryption completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")

def decrypt_button_click():
    try:
        input_file_path = entry_input_file.get()
        output_folder_path = entry_output_folder.get()

        private_key = load_key_from_file('private_key.pem')
        decrypt_file(private_key, input_file_path, output_folder_path + "/decrypted_file")
        messagebox.showinfo("Success", "Decryption completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("RSA Encryption/Decryption")

# Input File
label_input_file = tk.Label(root, text="Input File:")
entry_input_file = tk.Entry(root, width=40)
button_browse_input = tk.Button(root, text="Browse", command=lambda: browse_file(entry_input_file))

# Output Folder
label_output_folder = tk.Label(root, text="Output Folder:")
entry_output_folder = tk.Entry(root, width=40)
button_browse_output = tk.Button(root, text="Browse", command=lambda: browse_folder(entry_output_folder))

# Encrypt Button
button_encrypt = tk.Button(root, text="Encrypt", command=encrypt_button_click)

# Decrypt Button
button_decrypt = tk.Button(root, text="Decrypt", command=decrypt_button_click)

# Arrange widgets in the grid
label_input_file.grid(row=0, column=0, padx=10, pady=5)
entry_input_file.grid(row=0, column=1, padx=10, pady=5)
button_browse_input.grid(row=0, column=2, padx=10, pady=5)

label_output_folder.grid(row=1, column=0, padx=10, pady=5)
entry_output_folder.grid(row=1, column=1, padx=10, pady=5)
button_browse_output.grid(row=1, column=2, padx=10, pady=5)

button_encrypt.grid(row=2, column=0, columnspan=3, pady=10)
button_decrypt.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
