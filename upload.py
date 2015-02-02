import os.path
import time
from flask import Flask, redirect, request, render_template, url_for
from werkzeug import secure_filename

app = Flask(__name__)
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'upload/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# max file size 16M
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a new file."""
    if request.method == 'POST':
        # Get the name of the uploaded file
        fileset = request.files.getlist('photo')
        for file in fileset:
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to
                # the upload folder we setup
                filename = str(time.time()) + '.' + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)