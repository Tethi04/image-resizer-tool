1. What is PIL/Pillow?
PIL (Python Imaging Library) was the original library for image processing in Python. Pillow is the modern, friendly fork of PIL that is currently maintained. It supports opening, manipulating, and saving many different image file formats.

2. How do you open and save images?
from PIL import Image
img = Image.open("input.jpg")  # Open
img.save("output.png")         # Save

3. What is the resize() method?
resize() is a method in Pillow that takes a tuple (width, height) and returns a new copy of the image scaled to those specific dimensions.

4. How do you read all files in a directory?
You use the os module. Specifically, os.listdir(path) returns a list of all filenames in a folder.

5. What is the os module?
The os (Operating System) module provides a portable way of using operating system-dependent functionality, such as reading or writing to the file system, creating directories, and handling file paths.

6. How do you change file formats (e.g., JPG to PNG)?
In Pillow, you simply specify the new file extension in the .save() method. The library automatically converts the format.
img = Image.open("photo.jpg")
img.save("photo.png") # Automatically converts format

7. What is a pixel?
A pixel (Picture Element) is the smallest controllable element of a digital image. An image is essentially a grid of pixels, where each pixel has a specific color value.

8. What's the use of try-except here?
Image processing is prone to errors (corrupted files, unsupported formats, permission issues). A try-except block ensures that if one image fails, the script prints an error but continues processing the remaining images instead of crashing.

9. How can you make the app dynamic?
You could use input() to ask the user for their desired width and height instead of hardcoding (800, 800).

10. Can this be extended to GUI?
Yes! You can use libraries like Tkinter or PyQt to build a graphical interface where users can drag and drop images and click a "Resize" button, rather than using the command line.
