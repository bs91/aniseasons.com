from flask import request
from PIL import Image
from unicodedata import normalize

import os
import re


def resize_image(pic, max_width):
    im = Image.open(pic)
    dimensions = im.size

    width_percent = (max_width / float(dimensions[0]))
    new_height = int((float(dimensions[1]) * float(width_percent)))

    return im.resize((max_width, new_height), Image.ANTIALIAS)


def save_image_and_thumbnail(name, fileblob, path, full_width=600, thumb_width=194, ext='.jpg'):
    filename = name + ext
    thumb_filename = "thumb-" + filename

    full_image_path = os.path.join(path, filename)
    thumb_image_path = os.path.join(path, thumb_filename)

    image = resize_image(fileblob, full_width)
    image.save(full_image_path, 'JPEG', quality=95)
    thumb = resize_image(open(full_image_path), thumb_width)
    thumb.save(thumb_image_path, 'JPEG', quality=95)

    return filename, thumb_filename


def are_fields_valid(request, is_update=False):
    if len(request.form) > 0:
        if request.form['title'] and request.form['type'] and request.form['description']:
            if not is_update and request.files or is_update:
                return True

    return False

def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))
