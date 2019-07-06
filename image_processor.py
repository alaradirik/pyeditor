import argparse
import logging
import os
import subprocess
import sys

import pytesseract
from PIL import Image

DEFAULT_OUTPUT_DIRECTORY_NAME = "converted-text"
DEFAULT_CHECK_COMMAND = "which"
WINDOWS_CHECK_COMMAND = "where"
TESSERACT_DATA_PATH_VAR = 'TESSDATA_PREFIX'
VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".gif", ".png", ".tga", ".tif", ".bmp"]


def create_directory(path):
    """
        Create directory at given path if directory does not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def check_path(path):
    """
        Check if file path exists or not.
    """
    return bool(os.path.exists(path))

def get_command():
    """
        Check if tesseract is installed or not.
    """
    if sys.platform.startswith('win'):
        return WINDOWS_CHECK_COMMAND
    return DEFAULT_CHECK_COMMAND

def run_tesseract(filename, output_path, image_file_name):
    # Run tesseract
    filename_without_extension = os.path.splitext(filename)[0]
    text_file_path = os.path.join(output_path, filename_without_extension)
    text = pytesseract.image_to_string(Image.open(filename))
    print(text)

    """
    subprocess.run(['tesseract', image_file_name, text_file_path],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
    """
def check_pre_requisites_tesseract():
    """
        Check if the prerequisites for tesseract are satisfied or not.
    """
    check_command = get_command()
    logging.debug("Running `{}` to check if tesseract is installed or not.".format(check_command))

    result = subprocess.run([check_command, 'tesseract'], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error("Tesseract OCR is missing, install 'tesseract' to continue.")
        return False

    logging.debug("Tesseract correctly installed!\n")

    if sys.platform.startswith('win'):
        environment_variables = os.environ

        if TESSERACT_DATA_PATH_VAR in environment_variables:
            if environment_variables[TESSERACT_DATA_PATH_VAR]:
                path = environment_variables[TESSERACT_DATA_PATH_VAR]

                if os.path.isdir(path) and os.access(path, os.R_OK):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return True


def convert_image_to_text(input_path, output_path):
    if not check_pre_requisites_tesseract():
        return

    # Check if a valid input directory is given or not
    if not check_path(input_path):
        logging.error("Nothing found at `{}`".format(input_path))
        return

    create_directory(output_path)
    # Extract text from image with tesseract
    filename = os.path.basename(input_path)
    print(filename)
    run_tesseract(filename, output_path, filename)
