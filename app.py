from flask import Flask, render_template, request

import os

app = Flask(__name__)
app.config['UPLOADED_PATH'] = os.path.join(app.root_path, 'images/uploads')

### TODO: mkdir -> images/uploads and images/processed
### TODO: process images -> crop and correct for skew, brightness

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        for file in request.files.getlist('file'):
            file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True)