import os
import re

from flask import Flask, render_template, request
import nltk
#from nltk.tokenize import sent_tokenize
#nltk.download('punkt')

from image_processor import convert_image_to_text


app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/images/uploads')
PROCESSED_DOC_FOLDER = os.path.join(app.root_path, 'static/images/processed')

### TODO: process uploaded images -> crop and correct for skew, brightness
### TODO: tesseract to text file -> read in line by line
def split_paragraph_into_sentences(paragraph):
    sentence_list = sent_tokenize(paragraph)
    return sentence_list

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        for file in request.files.getlist('file'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            file.save(filepath)

        return "OK"

    return render_template('index.html')

@app.route('/editor')
def serve_processed_image():
    valid_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
    filename = [fn for fn in os.listdir(UPLOAD_FOLDER)
              if any(fn.endswith(ext) for ext in valid_extensions)][0]
    filepath = os.path.join('/static/images/uploads', filename)
    
    convert_image_to_text(UPLOAD_FOLDER, PROCESSED_DOC_FOLDER)

    return render_template('editor.html', filepath=filepath)

if __name__ == "__main__":
    app.run(debug = True)
