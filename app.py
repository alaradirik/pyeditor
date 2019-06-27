import os
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/images/uploads')
print(UPLOAD_FOLDER)

### TODO: process uploaded images -> crop and correct for skew, brightness
### TODO: extract text from processed images

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

    return render_template('editor.html', filepath=filepath)


if __name__ == "__main__":
    app.run(debug = True)