from flask import Flask, render_template, request

import os

app = Flask(__name__)
app.config['UPLOADED_PATH'] = os.path.join(app.root_path, 'images/uploads')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        for file in request.files.getlist('file'):
            file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))
    return render_template('index.html')


@app.route("/identify")
def identify():
    faceRecognizer = FaceRecognizer(
        source=0,
        haar_file=HAAR_FILE,
        data_path=DATA_PATH,
        width=WIDTH,
        height=HEIGHT
    )
    user_name = faceRecognizer.identify_user()
    print(user_name)
    return render_template("confirm.html", name=user_name)


if __name__ == "__main__":
    app.run(debug = True)