import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import module as md

app =  Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = set(["pdf"])
app.config["UPLOAD_FOLDERS"] = "uploads/"

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1] in app.config["ALLOWED_EXTENSIONS"]
    )

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        document = request.files["file"]
        if document and allowed_file(document.filename):
            filename = secure_filename(document.filename)
            document.filename.replace(' ', '_')
            document.save(os.path.join(app.config["UPLOAD_FOLDERS"], filename))
            document_file = os.path.join(app.config["UPLOAD_FOLDERS"], filename)
            preprocessed = md.preprocessing(document_file)
            document_stores = md.document_store(preprocessed)
            qag_pipeline = md.question_generator_pipeline(document_stores)
            file_excel = md.question_generator(document_stores, qag_pipeline)
            return render_template("result.html", file_excel=file_excel)
        else:
            return render_template("index.html", message="Please upload a PDF file!")    
    else:
        return render_template("index.html", message="Please upload a PDF file!")

@app.route("/download_excel/<excel>")
def download_excel(excel):
    excel = 'static/'+excel
    print(excel)
    return send_file(excel, as_attachment=True)

if __name__ == "__main__":
    app.run(
        debug=True
    )
