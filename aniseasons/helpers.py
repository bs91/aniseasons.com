from PIL import Image

def resize_image(pic, max_width):
    im = Image.open(pic)
    dimensions = im.size

    width_percent = (max_width / float(dimensions[0]))
    new_height = int((float(dimensions[1]) * float(width_percent)))

    return im.resize((max_width, new_height), Image.ANTIALIAS)
