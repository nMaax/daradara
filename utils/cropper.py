from PIL import Image
import os

def crop_mantain_aspect_ratio(path):
    image = Image.open(path)
    new_image = make_square(image)
    save_path = os.path.join(os.path.dirname(path), "resized_" + os.path.basename(path))
    new_image.save(save_path)

def make_square(im, min_size=256, fill_color=(255, 255, 255)): # fill_color=(248, 249, 250) per i colori light di bs
    im = Image.open(im)
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im