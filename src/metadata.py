"""Library of funtions to extract metadata from files"""

from exif import Image as exif_image
from PIL import Image as pil_image
from PyPDF2 import PdfFileReader
from docx import Document

@staticmethod
def get_exif_metadata(file):
    """Function returns dict with metadata"""
    with open(file, 'rb') as file_handler:
        info = exif_image(file_handler)
    if info.has_exif:
        return {
            "copyright": info.copyright,
            "datetime": info.datetime,
            "datetime_original": info.datetime_original,
            "camera_model": info.model,
            "shutter_speed": info.shutter_speed_value,
            "software": info.software
        }
    return None

@staticmethod
def get_pillow_metadata(file):
    """Function returns dict with metadata"""
    with open(file, 'rb') as file_handler:
        info = pil_image.open(file_handler)
    return {
        "image_height": info.height,
        "image_width": info.width,
        "image_format": info.format,
        "image_mode": info.mode
    }

@staticmethod
def status_exif_data(file):
    """Function returns if metadata exists"""
    with open(file, 'rb') as file_handler:
        info = pil_image.open(file_handler)
    info.close()
    if info.info.get("exif"):
        return True
    return False

@staticmethod
def get_pdf_metadata(file):
    """Function returns dict with metadata"""
    with open(file, 'rb') as file_handler:
        doc = PdfFileReader(file_handler)
        info = doc.getDocumentInfo()
    return {
        "author": info.author,
        "creator":  info.creator,
        "producer": info.producer,
        "subject":  info.subject,
        "title": info.title,
        "creation_date": info['/CreationDate'],
        "modification_date": info['/ModDate']
    }

@staticmethod
def get_docx_metadata(file):
    """Function returns dict with metadata"""
    document = Document(file)
    info = document.core_properties
    return {
        "author": info.author,
        "last_modified_by": info.last_modified_by,
        "creation_date": \
        str(info.created.year) + '/' + str(info.created.month) + '/' + str(info.created.day),
        "last_modification_date": \
        str(info.modified.year) + '/' + str(info.modified.month) + '/' + str(info.modified.day)
    }
