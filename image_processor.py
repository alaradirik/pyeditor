import argparse
import logging
import os
import subprocess
import sys


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

    subprocess.run(['tesseract', image_file_name, text_file_path],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)

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

    if not check_path(input_path):
        logging.error("Nothing found at `{}`".format(input_path))
        return

    create_directory(output_path)

    # Check if input_path is directory or file
    if os.path.isdir(input_path):

        # Check if input directory is empty or not
        total_file_count = len(os.listdir(input_path))
        if total_file_count == 0:
            logging.error("No files found at your input location")
            return

        # Iterate over all images in the input directory
        # and get text from each image
        other_files = 0
        successful_files = 0
        logging.info("Found total {} file(s)\n".format(total_file_count))
        for ctr, filename in enumerate(os.listdir(input_path)):
            logging.debug("Parsing {}".format(filename))
            extension = os.path.splitext(filename)[1]

            if extension.lower() not in VALID_IMAGE_EXTENSIONS:
                other_files += 1
                continue

            image_file_name = os.path.join(input_path, filename)
            run_tesseract(filename, output_path, image_file_name)
            successful_files += 1

        logging.info("Parsing Completed!\n")
        if successful_files == 0:
            logging.error("No valid image file found.")
            logging.error("Supported formats: [{}]".format(
                ", ".join(VALID_IMAGE_EXTENSIONS)))
        else:
            logging.info(
                "Successfully parsed images: {}".format(successful_files))
            logging.info(
                "Files with unsupported file extensions: {}".format(other_files))

    else:
        filename = os.path.basename(input_path)
        run_tesseract(filename, output_path, filename)

