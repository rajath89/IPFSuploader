import os
import ipfsapi
# api = ipfsapi.connect('https://ipfs.infura.io', 5001)
api = ipfsapi.connect('127.0.0.1', 5001)
from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
from werkzeug.utils import secure_filename
image =''
image_hash = ''
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'zip', 'mp3', 'mp4', 'flv','mkv'])

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("upload.html")


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadPic', methods=['GET', 'POST'])
def uploadPic():
    target = os.path.join(APP_ROOT, 'up_images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        # check if the post request has the file part

        if 'file' not in request.files:
            print('No File Part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser submits an empty part
        # without filename
        if file.filename == '':
            print('No Selected File')
            return jsonify({'Response': "No file was selected. Please Select a Valid File and Try Again"})
        # if file and allowed_file(file.filename):
        if file:
            res = api.add(file)
            print(res['Hash'])
            image = 'http://127.0.0.1:8080/ipfs/'+ res['Hash']
            image_hash = res['Hash']
            filename = secure_filename(file.filename)
            destination = "/".join([target, filename])
            file.save(destination)
            return render_template("image.html", **locals())
        else:
            return jsonify({'Response': 'FAILED. Make sure it is an image or a zip file'})
    return render_template("upload.html")


@app.route('/uploadPic/<filename>', methods=['GET'])
def uploaded_file(filename):
    target = os.path.join(APP_ROOT, 'up_images/')
    if filename in target:
        return send_from_directory(target, filename)
    else:
        return jsonify({'Response': "File Does Not Exist"})

if __name__ == '__main__':
    app.run(debug=True)
