# I Asked ChatGPT to Create Simple Image Processing Code
::tags{Image Processing, ChatGPT}::

---

I scanned a hand-drawn picture, but I don't have any good image editing software, so I can't edit it...  
For people like me, here's a way to create Python code for image editing using ChatGPT.  
This time, I'll use the method I used to create the icon image for this site as an example.


## What Image Editing Operation Are We Trying to Do This Time?
We'll use the task of inverting the black-and-white colors of a hand-drawn picture and making the originally white parts transparent.  
This is what I actually did to create the icon image for this site.

::img{
    file{
        hitbug-icon.png: Cute icon drawing;
    }
    height: 250px;
}::

## How Did You Ask ChatGPT?
I asked like this:
```
Please create Python code using Pillow to perform the following processing.

# Processing
1. Load the image (icon_black.png) and define it as a.
2. Binarize a using a threshold of 150 for brightness and define it as b.
3. Invert the black-and-white colors of b and define it as c.
4. Change the black areas in c to transparent and define it as d.
5. Output d as icon_white.png.
```
Then, it returned working code in one request.  
[Here is the conversation we had](https://chat.openai.com/share/18dcb15d-6e59-46b4-9348-519cb11f740b).  
Writing Japanese that conveys the image of the program increases accuracy.
```
from PIL import Image

# Load the image
a = Image.open("icon_black.png")

# Binarize the image
b = a.convert("L").point(lambda x: 255 if x > 150 else 0, mode='1')

# Invert the black-and-white colors
c = Image.eval(b, lambda x: 255 - x)

# Change the black areas to transparent
d = c.convert("RGBA")
data = d.getdata()
new_data = []
for item in data:
    # Change the black areas to transparent
    if item[0] == 0 and item[1] == 0 and item[2] == 0:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)
d.putdata(new_data)

# Output the image
d.save("icon_white.png")
```

But what if you don't know terms like brightness or binarization?  
I think I'll write an article for those people in the future.


## Side Note
I once used a paid image processing software for work ~~because I had to~~, and I remember that almost everything could be implemented quickly with Python.  
Knowing the terms and implementation can save you quite a bit!


## Summary
For those who don't have good image editing software, I introduced a method to create Python code for image editing using ChatGPT.  
I hope it serves as a reference for someone.