#!/usr/bin/env python3
"""
Image Steganography Tool
Hides text or files inside images using LSB (Least Significant Bit) technique
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import os


class SteganographyTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool - Hide Data in Images")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        self.image_path = None
        self.output_path = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="🔐 Image Steganography Tool",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Embed Tab
        self.embed_frame = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.embed_frame, text="Embed Data")
        self.create_embed_tab()
        
        # Extract Tab
        self.extract_frame = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.extract_frame, text="Extract Data")
        self.create_extract_tab()
        
        # Info label
        info_label = tk.Label(
            self.root,
            text="Supported formats: PNG, BMP | Drag & drop images onto buttons",
            font=("Arial", 9, "italic"),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        info_label.pack(pady=5)
    
    def create_embed_tab(self):
        # Image selection section
        image_frame = tk.LabelFrame(
            self.embed_frame,
            text="1. Select Cover Image",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            padx=20,
            pady=15
        )
        image_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.embed_image_btn = tk.Button(
            image_frame,
            text="📁 Choose Image (PNG/BMP)",
            command=self.select_cover_image,
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.embed_image_btn.pack(pady=5)
        self.embed_image_btn.drop_target_register(DND_FILES)
        self.embed_image_btn.dnd_bind('<<Drop>>', self.drop_cover_image)
        
        self.embed_image_label = tk.Label(
            image_frame,
            text="No image selected",
            font=("Arial", 9),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        self.embed_image_label.pack()
        
        # Message section
        msg_frame = tk.LabelFrame(
            self.embed_frame,
            text="2. Enter Secret Message",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            padx=20,
            pady=15
        )
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.message_text = tk.Text(
            msg_frame,
            height=8,
            font=("Courier", 10),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Or file selection
        tk.Label(
            msg_frame,
            text="OR",
            font=("Arial", 9, "bold"),
            bg="#ffffff"
        ).pack(pady=5)
        
        self.file_btn = tk.Button(
            msg_frame,
            text="📎 Choose File to Hide",
            command=self.select_file_to_hide,
            font=("Arial", 9),
            bg="#95a5a6",
            fg="white",
            cursor="hand2"
        )
        self.file_btn.pack()
        
        self.file_label = tk.Label(
            msg_frame,
            text="No file selected",
            font=("Arial", 8),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        self.file_label.pack(pady=2)
        
        # Embed button
        embed_btn = tk.Button(
            self.embed_frame,
            text="🔒 Embed Data",
            command=self.embed_data,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=12,
            cursor="hand2"
        )
        embed_btn.pack(pady=15)
    
    def create_extract_tab(self):
        # Image selection
        image_frame = tk.LabelFrame(
            self.extract_frame,
            text="1. Select Stego Image",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            padx=20,
            pady=15
        )
        image_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.extract_image_btn = tk.Button(
            image_frame,
            text="📁 Choose Stego Image",
            command=self.select_stego_image,
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.extract_image_btn.pack(pady=5)
        self.extract_image_btn.drop_target_register(DND_FILES)
        self.extract_image_btn.dnd_bind('<<Drop>>', self.drop_stego_image)
        
        self.extract_image_label = tk.Label(
            image_frame,
            text="No image selected",
            font=("Arial", 9),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        self.extract_image_label.pack()
        
        # Extract button
        extract_btn = tk.Button(
            self.extract_frame,
            text="🔓 Extract Data",
            command=self.extract_data,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=12,
            cursor="hand2"
        )
        extract_btn.pack(pady=20)
        
        # Result display
        result_frame = tk.LabelFrame(
            self.extract_frame,
            text="Extracted Data",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            padx=20,
            pady=15
        )
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_text = tk.Text(
            result_frame,
            height=10,
            font=("Courier", 10),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def select_cover_image(self):
        path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("PNG files", "*.png"), ("BMP files", "*.bmp"), ("All files", "*.*")]
        )
        if path:
            self.image_path = path
            self.embed_image_label.config(text=os.path.basename(path))
    
    def drop_cover_image(self, event):
        path = event.data.strip('{}')
        if path.lower().endswith(('.png', '.bmp')):
            self.image_path = path
            self.embed_image_label.config(text=os.path.basename(path))
    
    def select_stego_image(self):
        path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("PNG files", "*.png"), ("BMP files", "*.bmp"), ("All files", "*.*")]
        )
        if path:
            self.output_path = path
            self.extract_image_label.config(text=os.path.basename(path))
    
    def drop_stego_image(self, event):
        path = event.data.strip('{}')
        if path.lower().endswith(('.png', '.bmp')):
            self.output_path = path
            self.extract_image_label.config(text=os.path.basename(path))
    
    def select_file_to_hide(self):
        path = filedialog.askopenfilename(title="Select File to Hide")
        if path:
            with open(path, 'rb') as f:
                data = f.read()
            # Store filename and data
            filename = os.path.basename(path)
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(1.0, f"FILE:{filename}:" + data.hex())
            self.file_label.config(text=f"File: {filename} ({len(data)} bytes)")
    
    def text_to_binary(self, text):
        """Convert text to binary string"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    def binary_to_text(self, binary):
        """Convert binary string to text"""
        chars = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))
        return ''.join(chars)
    
    def embed_data(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select a cover image first!")
            return
        
        message = self.message_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message or select a file!")
            return
        
        try:
            # Load image
            img = Image.open(self.image_path)
            
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
            
            # Add delimiter
            message = message + "<<<END>>>"
            binary_message = self.text_to_binary(message)
            
            # Check if message fits
            pixels = list(img.getdata())
            max_bytes = len(pixels) * 3 // 8
            if len(binary_message) > len(pixels) * 3:
                messagebox.showerror(
                    "Error",
                    f"Message too large! Maximum {max_bytes} bytes, got {len(message)} bytes."
                )
                return
            
            # Embed data
            data_index = 0
            new_pixels = []
            
            for pixel in pixels:
                if isinstance(pixel, int):
                    pixel = (pixel, pixel, pixel)
                
                r, g, b = pixel[:3]
                
                if data_index < len(binary_message):
                    r = (r & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                
                if data_index < len(binary_message):
                    g = (g & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                
                if data_index < len(binary_message):
                    b = (b & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                
                if len(pixel) == 4:
                    new_pixels.append((r, g, b, pixel[3]))
                else:
                    new_pixels.append((r, g, b))
            
            # Create output image
            stego_img = Image.new(img.mode, img.size)
            stego_img.putdata(new_pixels)
            
            # Save
            output_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("BMP files", "*.bmp")]
            )
            
            if output_path:
                stego_img.save(output_path)
                messagebox.showinfo(
                    "Success",
                    f"Data successfully embedded!\nSaved to: {os.path.basename(output_path)}"
                )
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to embed data: {str(e)}")
    
    def extract_data(self):
        if not self.output_path:
            messagebox.showerror("Error", "Please select a stego image first!")
            return
        
        try:
            # Load image
            img = Image.open(self.output_path)
            
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
            
            pixels = list(img.getdata())
            
            # Extract binary data
            binary_data = ""
            for pixel in pixels:
                if isinstance(pixel, int):
                    pixel = (pixel, pixel, pixel)
                
                r, g, b = pixel[:3]
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)
            
            # Convert to text
            extracted_text = self.binary_to_text(binary_data)
            
            # Find delimiter
            if "<<<END>>>" in extracted_text:
                extracted_text = extracted_text.split("<<<END>>>")[0]
            else:
                messagebox.showwarning(
                    "Warning",
                    "Delimiter not found. This may not be a valid stego image."
                )
            
            # Check if it's a file
            if extracted_text.startswith("FILE:"):
                parts = extracted_text.split(":", 2)
                if len(parts) == 3:
                    filename = parts[1]
                    hex_data = parts[2]
                    
                    # Ask where to save
                    save_path = filedialog.asksaveasfilename(
                        defaultextension="",
                        initialfile=filename
                    )
                    
                    if save_path:
                        file_data = bytes.fromhex(hex_data)
                        with open(save_path, 'wb') as f:
                            f.write(file_data)
                        
                        self.result_text.config(state=tk.NORMAL)
                        self.result_text.delete(1.0, tk.END)
                        self.result_text.insert(
                            1.0,
                            f"File extracted successfully!\nSaved to: {save_path}\nSize: {len(file_data)} bytes"
                        )
                        self.result_text.config(state=tk.DISABLED)
                        messagebox.showinfo("Success", "File extracted successfully!")
                return
            
            # Display extracted text
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, extracted_text)
            self.result_text.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", "Data extracted successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract data: {str(e)}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SteganographyTool(root)
    root.mainloop()
