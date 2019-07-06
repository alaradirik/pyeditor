# editorX

## Background

EditorX is an image-to-text web app that allows users to edit extracted text and save it as pdf.

## Project Structure

    .
    ├── app.py                   # EditorX Flask app
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

#### Install pre-commit hook so black will autorun on commits

`pre-commit install`

#### Install Tesseract OCR





## Running EditorX: