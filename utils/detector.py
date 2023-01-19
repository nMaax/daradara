IMG_EXTENSIONS = ('.jpeg', '.jpg', '.png', '.gif')
AUDIO_EXTENSIONS = ('.mp3', '.wav')

def is_static_image(filename):
    """
    Returns a boolean expressing if the filename is a static image (.png or .jpeg/.jpg) or not
    """

    return is_image(filename) and not filename.endswith('.gif')

def is_image(filename):
    """
    Returns a boolean expressing if the filename is an image (.png or .jpeg/.jpg or .gif) or not
    """

    result = False
    for ext in IMG_EXTENSIONS:
        result |= filename.endswith(ext)
    return result

def is_audio(filename):
    """
    Returns a boolean expressing if the filename is an audio (.mp3 or .wav) or not
    """

    result = False
    for ext in AUDIO_EXTENSIONS:
        result |= filename.endswith(ext)
    return result