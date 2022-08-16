"""Library of funtions to extract metadata from files"""

from exif import Image as exif_image
from PIL import Image as pil_image

@staticmethod
def get_exif_metadata(file):
    """Function returns dict with metadata"""
    with open(file, 'rb') as file_handler:
        metadata = exif_image(file_handler)
    if metadata.has_exif:
        return {
            "copyright": metadata.copyright,
            "datetime": metadata.datetime,
            "datetime_original": metadata.datetime_original,
            "camera_model": metadata.model,
            "shutter_speed": metadata.shutter_speed_value,
            "software": metadata.software
        }
    return None

@staticmethod
def get_pillow_metadata(file):
    """Function returns dict with metadata"""
    with open(file, 'rb') as file_handler:
        metadata = pil_image.open(file_handler)
    return {
        "image_height": metadata.height,
        "image_width": metadata.width,
        "image_format": metadata.format,
        "image_mode": metadata.mode
    }

@staticmethod
def status_exif_data(file):
    """Function returns if metadata exists"""
    with open(file, 'rb') as file_handler:
        metadata = pil_image.open(file_handler)
    metadata.close()
    if metadata.info.get("exif"):
        return True
    return False
