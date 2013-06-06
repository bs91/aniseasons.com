from flask import request
from PIL import Image
from unicodedata import normalize

import re


def resize_image(pic, max_width):
    im = Image.open(pic)
    dimensions = im.size

    width_percent = (max_width / float(dimensions[0]))
    new_height = int((float(dimensions[1]) * float(width_percent)))

    return im.resize((max_width, new_height), Image.ANTIALIAS)


def are_fields_valid(request):
    if request.files and request.form['title'] and request.form['type'] and request.form['description']:
        return True
    else:
        return False

def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))
