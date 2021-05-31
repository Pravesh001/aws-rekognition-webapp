import os
import boto3
import csv
from flask import *  

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

#readinng aws keys
#with open('pravesh_api_new_user_credentials.csv', 'r') as input:
#    next(input) #goto second line
#    reader = csv.reader(input)
#    for line in reader:
#        access_key_id = line[2] #see file .csv
#        secret_access_key = line[3]
access_key_id = 'AKIAX6EPIEM6W7IYB5XF'
secret_access_key = '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'

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
     
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))  
        file_n = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        client = boto3.client ('rekognition', aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key)
        photo = file_n
        with open(photo,'rb') as source_image:
            source_bytes = source_image.read() #get photo in bytes
        response = client.detect_faces(Image = {'Bytes': source_bytes},Attributes = ['ALL'])
        return render_template("success.html",user_image = file_n, name = response )  
      
if __name__ == '__main__':  
    app.run(host = '0.0.0.0', port=80)  
