# editorX

## Background

EditorX is an image-to-text web app that allows users to edit extracted text and save it as pdf.

![working app](https://github.com/alaradirik/editorX/blob/master/screenshots/app.gif "Flask app")

## Project Structure

    .
    ├── app.py
    ├── image_processor.py              # Extracts text from images
    ├── static                          # Includes CSS, JS and image folders
        └── css
        └── js
        └── image
            └── uploads
            └── processed
    ├── templates                       # HTML files
    ├── requirements.txt   
    ├── LICENCE          
    └── README.md

## Installation Instructions

#### Create your python environment. If using conda:

`conda create -n [name of enviroment] python=3.7`

#### Installation of dependencies:

`pip install -r requirements.txt`

#### Install Tesseract OCR:

Linux:
`[sudo] apt-get install tesseract-ocr`

macOS:
`brew install tesseract-ocr`

Windows:
Find the instructions [here.](https://github.com/tesseract-ocr/tesseract/wiki)



## Running EditorX:

`python app.py`