################################
#    used for image beauty
#   impleted here because images need transfer to electron main process to save
#   that will block the main process, this is unfriendly for user

from PIL import Image, ImageEnhance

def brightnessImage(imgData, val):
    """
    birghtness
    """
    if not imgData:
        return None
    if not isinstance(val):
        try:
            val = float(val)
        except ValueError:
            return None
    return ImageEnhance.Brightness(imgData).enhance(val)


def contrastImage(imgData, val):
    """
    contrast
    """
    if not imgData:
        return None
    if not isinstance(val):
        try:
            val = float(val)
        except ValueError:
            return None
    return ImageEnhance.Contrast(imgData).enhance(val)
