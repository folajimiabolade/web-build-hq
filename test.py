from flask import Flask, flash, redirect, url_for, request, render_template
import os
from werkzeug.utils import secure_filename

allowed_extensions = {"txt", "pdf", "jpg", "jpeg", "png", "gif", "mp3", "mp4"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images/uploads"
app.config["MAX_CONTENT_LENGTH"] = 2 * 1000 * 1000


def valid_extension(filename):
    if "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions:
        return True

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "picture" not in request.files:
            print("no file part")
            return redirect(url_for("upload_file"))
        print(request.files)
        file = request.files["picture"]
        if file.filename == "":
            print("the user did not select a file")
            return redirect(url_for("upload_file"))
        if file and valid_extension(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("upload_file"))
    return render_template("test.html")
if __name__ == "__main__":
    app.run(debug=True)

# import re
#
# text = "Hello_world-123.jpg!"
# bad_chars = re.findall(r'[^a-z0-9_.-]', text)
# print(bad_chars)