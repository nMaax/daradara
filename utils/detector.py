IMG_EXTENSIONS = ('.jpeg', '.jpg', '.png', '.gif')
AUDIO_EXTENSIONS = ('.mp3', '.wav')

def is_static_image(filename):
    return is_image(filename) and not filename.endswith('.gif')

def is_image(filename):
    result = False
    for ext in IMG_EXTENSIONS:
        result |= filename.endswith(ext)
    return result

def is_audio(filename):
    result = False
    for ext in AUDIO_EXTENSIONS:
        result |= filename.endswith(ext)
    return result