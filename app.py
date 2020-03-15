import os
import re
import html

from flask import Flask, render_template, request
from extract_text import convert_image_to_text, read_text
from correct_image import transform_image


app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, "static/images/uploads")
PROCESSED_DOC_FOLDER = os.path.join(app.root_path, "static/images/processed")

### TODO: process uploaded images -> crop and correct for skew, brightness
### TODO: clean up extracted text and break into paragraphs

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":

        for file in request.files.getlist("file"):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(filepath)
            transform_image(filepath)

        return "OK"

    return render_template("index.html")

@app.route("/editor")
def serve_processed_image():
    valid_extensions = ["jpg","jpeg", "bmp", "png", "gif"]
    filename = [fn for fn in os.listdir(UPLOAD_FOLDER)
              if any(fn.endswith(ext) for ext in valid_extensions)][0]
    filepath = os.path.join("/static/images/uploads", filename)
    
    convert_image_to_text(UPLOAD_FOLDER, PROCESSED_DOC_FOLDER)
    text = read_text(PROCESSED_DOC_FOLDER)[0]


    return render_template("editor.html", filepath=filepath, text=text)

if __name__ == "__main__":
    app.run(debug = True)
