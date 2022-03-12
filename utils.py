import os
from PIL import Image

def getDominantColor(iconPath):
    """Receives iconPath to get most used color in that icon and returns a string of rgb value"""
 
    # Get width and height of Image
    img = Image.open(iconPath)
    img = img.convert('RGB')
    img = img.resize((30, 30))
    width, height = img.size
 
    # Save all the color form each pixel
    listOfColors = []
    # Iterate through each pixel
    count = 0
    for x in range(0, width):
        for y in range(0, height):
            rgb = img.getpixel((x, y))
            if rgb != (0, 0, 0) and rgb != (255, 255, 255):
                count += 1
                listOfColors.append(rgb)
 
    #return most used color using set to check most common value avail in listOfColors
    final_color = max(set(listOfColors), key=listOfColors.count)
    if not isinstance(final_color, tuple):
        return (0, 0, 0)

    return f"rgb{final_color}"

def isIconLocallyAvail(iconPath):
    """Check if icon is already saved locally. so we dont have to make a URL request to save the icon"""
    
    if os.path.exists(iconPath):
        return True
    return False

def getIconData(iconPath):
    """This function checks if the icon is avail in icons folder, If not it will cal saveIcon method to save teh icon.
    It receives icon URL and returns the icon path from the cryptoIcon folder"""
    
    if os.path.exists(iconPath):
        with open(iconPath, "rb") as iconFile:
            iconData = iconFile.read()
            return iconData