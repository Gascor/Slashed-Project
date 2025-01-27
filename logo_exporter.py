from PIL import Image

def white_to_transparent(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        # Convert white (also near white) to transparent
        if item[0] > 200 and item[1] > 200 and item[2] > 200 and item[3] > 200:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    image.putdata(newData)
    image.save(output_path)
    
def black_to_transparent(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        # Convert black (and near black) to transparent
        if item[0] < 50 and item[1] < 50 and item[2] < 50:  # Adjust the threshold as needed
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    image.putdata(newData)
    image.save(output_path)

def transparent_to_black(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        # Convert transparent pixels to black
        if item[3] == 0:  # Check if the alpha channel (transparency) is 0
            newData.append((0, 0, 0, 255))  # Change to black, fully opaque
        else:
            newData.append(item)

    image.putdata(newData)
    image.save(output_path)
from PIL import Image

def white_to_black(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        # Change white pixels to black
        if item[0] > 200 and item[1] > 200 and item[2] > 200:  # Check if the pixel is white or near white
            newData.append((0, 0, 0, 255))  # Change to black
        else:
            newData.append(item)

    image.putdata(newData)
    image.save(output_path)

# Usage example
transparent_to_black("WT-TB_2024_Logo.png", "WT-BB_2024_Logo.png")
# Usage example
black_to_transparent("BT-WB_2024_Logo.png", "TT-WB_2024_Logo.png")
# Usage example
white_to_transparent("WT-BB_2024_Logo.png", "TT-BB_2024_Logo.png")
