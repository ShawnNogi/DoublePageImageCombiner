import tkinter as tk
from tkinter import filedialog
import os
from tkinterdnd2 import *
from PIL import Image
from datetime import datetime

def validate_image_file(path):
    """Check if the file is a valid image (PNG, JPG, JPEG)."""
    valid_extensions = ('.png', '.jpg', '.jpeg')
    return os.path.isfile(path) and os.path.splitext(path)[1].lower() in valid_extensions

def validate_dimensions(width, height):
    """Check if width and height are positive integers."""
    try:
        w, h = int(width), int(height)
        return w > 0 and h > 0
    except ValueError:
        return False

def get_image_dimensions(path):
    """Get image width and height using PIL."""
    try:
        with Image.open(path) as img:
            return img.size  # Returns (width, height)
    except Exception:
        return None

def combine_images_side_by_side(image_path1, image_path2, output_path, width, height):
    """Combine two images side-by-side."""
    try:
        img1 = Image.open(image_path1)
        img2 = Image.open(image_path2)
        if img1.size[1] != height or img2.size[1] != height:
            return f"Error: Both images must have height {height} pixels."
        if img1.size[0] != width or img2.size[0] != width:
            return f"Error: Both images must have width {width} pixels."
        combined_width = width * 2
        combined_height = height
        combined_image = Image.new('RGB', (combined_width, combined_height))
        combined_image.paste(img1, (0, 0))
        combined_image.paste(img2, (width, 0))
        combined_image.save(output_path)
        return f"Combined image saved as {output_path}"
    except Exception as e:
        return f"Error: Failed to combine images: {str(e)}"

def on_drop(event, entry):
    """Handle drag-and-drop event for an entry field."""
    try:
        data = event.widget.tk.splitlist(event.data)
        if data:
            file_path = data[0].strip('{}').replace('/', '\\')
            if validate_image_file(file_path):
                entry.delete(0, tk.END)
                entry.insert(0, file_path)
                if entry == entry1:  # First image sets dimensions
                    dims = get_image_dimensions(file_path)
                    if dims:
                        entry_width.delete(0, tk.END)
                        entry_width.insert(0, str(dims[0]))
                        entry_height.config(state="normal")
                        entry_height.delete(0, tk.END)
                        entry_height.insert(0, str(dims[1]))
                        entry_height.config(state="readonly")
                        status_label.config(text=f"Set dimensions: {dims[0]}x{dims[1]}")
                    else:
                        status_label.config(text="Error: Unable to read first image dimensions.", fg="red")
                elif entry == entry2:  # Validate second image
                    dims = get_image_dimensions(file_path)
                    if dims:
                        try:
                            first_height = int(entry_height.get())
                            if dims[1] != first_height:
                                status_label.config(text=f"Error: Second image height ({dims[1]}) does not match first ({first_height}).", fg="red")
                            else:
                                status_label.config(text=f"Second image height matches: {dims[1]} pixels")
                        except ValueError:
                            status_label.config(text="Error: Invalid height in first image field.", fg="red")
                    else:
                        status_label.config(text="Error: Unable to read second image dimensions.", fg="red")
            else:
                status_label.config(text="Error: Drop a valid image file (PNG, JPG, JPEG).", fg="red")
    except Exception as e:
        status_label.config(text=f"Error: Invalid drop: {str(e)}", fg="red")

def select_image1():
    path = filedialog.askopenfilename(
        initialdir=os.path.expanduser("~"),
        title="Select First Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    if path:
        entry1.delete(0, tk.END)
        entry1.insert(0, path)
        dims = get_image_dimensions(path)
        if dims:
            entry_width.delete(0, tk.END)
            entry_width.insert(0, str(dims[0]))
            entry_height.config(state="normal")
            entry_height.delete(0, tk.END)
            entry_height.insert(0, str(dims[1]))
            entry_height.config(state="readonly")
            status_label.config(text=f"Set dimensions: {dims[0]}x{dims[1]}")
        else:
            status_label.config(text="Error: Unable to read first image dimensions.", fg="red")

def select_image2():
    path = filedialog.askopenfilename(
        initialdir=os.path.expanduser("~"),
        title="Select Second Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    if path:
        entry2.delete(0, tk.END)
        entry2.insert(0, path)
        dims = get_image_dimensions(path)
        if dims:
            try:
                first_height = int(entry_height.get())
                if dims[1] != first_height:
                    status_label.config(text=f"Error: Second image height ({dims[1]}) does not match first ({first_height}).", fg="red")
                else:
                    status_label.config(text=f"Second image height matches: {dims[1]} pixels")
            except ValueError:
                status_label.config(text="Error: Invalid height in first image field.", fg="red")
        else:
            status_label.config(text="Error: Unable to read second image dimensions.", fg="red")

def combine_images():
    img1 = entry1.get()
    img2 = entry2.get()
    width = entry_width.get()
    height = entry_height.get()
    if not img1 or not img2:
        status_label.config(text="Error: Please select exactly two images.", fg="red")
        return
    if not validate_image_file(img1) or not validate_image_file(img2):
        status_label.config(text="Error: Invalid image files selected.", fg="red")
        return
    if not validate_dimensions(width, height):
        status_label.config(text="Error: Width and height must be positive integers.", fg="red")
        return
    try:
        width, height = int(width), int(height)
        output_dir = os.path.dirname(img1)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"combined_image_{timestamp}.jpg")
        result = combine_images_side_by_side(img1, img2, output_file, width, height)
        if result.startswith("Error"):
            status_label.config(text=result, fg="red")
        else:
            status_label.config(text=result, fg="green")
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
    except Exception as e:
        status_label.config(text=f"Error: Failed to combine images: {str(e)}", fg="red")

# Create GUI window
root = TkinterDnD.Tk()
root.title("Image Combiner")
root.geometry("600x350")

# Image selection
tk.Label(root, text="First Image:").grid(row=0, column=0, padx=10, pady=10)
entry1 = tk.Entry(root, width=50)
entry1.grid(row=0, column=1, padx=10)
tk.Button(root, text="Browse", command=select_image1).grid(row=0, column=2, padx=10)
entry1.drop_target_register(DND_FILES)
entry1.dnd_bind('<<Drop>>', lambda e: on_drop(e, entry1))

tk.Label(root, text="Second Image:").grid(row=1, column=0, padx=10, pady=10)
entry2 = tk.Entry(root, width=50)
entry2.grid(row=1, column=1, padx=10)
tk.Button(root, text="Browse", command=select_image2).grid(row=1, column=2, padx=10)
entry2.drop_target_register(DND_FILES)
entry2.dnd_bind('<<Drop>>', lambda e: on_drop(e, entry2))

# Dimension inputs
tk.Label(root, text="Image Width (pixels):").grid(row=2, column=0, padx=10, pady=10)
entry_width = tk.Entry(root, width=10)
entry_width.grid(row=2, column=1, sticky="w", padx=10)

tk.Label(root, text="Image Height (pixels):").grid(row=3, column=0, padx=10, pady=10)
entry_height = tk.Entry(root, width=10, state="readonly")
entry_height.grid(row=3, column=1, sticky="w", padx=10)

# Combine button
tk.Button(root, text="Combine Images", command=combine_images, width=20).grid(row=4, column=1, pady=10)

# Status label
status_label = tk.Label(root, text="", wraplength=500, fg="black")
status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Start GUI
root.mainloop()