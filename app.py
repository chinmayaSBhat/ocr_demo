#import packages
from flask import Flask
import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import sys
from PIL import Image
import uuid
import pytesseract

MYDIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) 
TEXT_FOLDER=os.path.join(MYDIR,'/media/texts')
UPLOAD_FOLDER=os.path.join(MYDIR,'/media/images')


ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}

application = Flask(__name__)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# limit upload size upto 8mb
application.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


application = Flask(__name__)

@application.route("/",methods=['GET', 'POST'])
#@application.route("/home",methods=['GET', 'POST'])
def index():
    path=''
    if request.method == 'POST':

        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            tname=str(uuid.uuid4())
            filename2=tname+'.png'	    
            file.save(os.path.join(application.config['UPLOAD_FOLDER'],filename2))         
            result = path.split("/")
            filename2 = result[-1:]
            print("fname :" ,filename2)
            filename1 = " ".join(filename2)  
            
            return redirect(url_for('result',image_path=tname))  
      
    return render_template('index1.html')
    

    


@application.route('/result/<image_path>')
def result(image_path):
    t=[]
    image_path+='.png'
    path=os.path.join(UPLOAD_FOLDER,image_path)
    content=pytesseract.image_to_string(path,lang='kan')
    t.append(content)
    t.append(image_path)
    return render_template('responsepage.html',content=t)
    
@application.route('/edit_results', methods=['POST'])
def edit_results():
    file_path=request.form['image_path']
    print("textfile:",file_path)
    text_file=TEXT_FOLDER+'/'+file_path[:-4]+'.txt'
    f = open(text_file, "w")
    content=file_path=request.form['text']
    f.write(content)
    f.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    #application.debug=True
    application.run()


















