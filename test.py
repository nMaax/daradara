from PIL import Image
import os

def crop_mantain_aspect_ratio(path):
    image = Image.open(path)
    new_image = make_square(image)
    save_path = os.path.join(os.path.dirname(path), "resized_" + os.path.basename(path))
    new_image.save(save_path)

def make_square(im, min_size=256, fill_color=(256, 256, 256)):
    x, y = im.size
    size = max(min_size, x, y)
    aspect_ratio = x/y
    if aspect_ratio>1:
        left = 0
        top = int((size - y) / 2)
    else:
        top = 0
        left = int((size - x) / 2)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (left, top))
    return new_im

def juan_make_square(post_image):
    img = Image.open(post_image)

    POST_IMG_WIDTH = img.width

    width, height = img.size
    new_height = int(height/width) * POST_IMG_WIDTH
    size = POST_IMG_WIDTH, new_height

    img.thumbnail(size, Image.ANTIALIAS)
