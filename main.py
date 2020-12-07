import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from keras.applications.xception import Xception
# from keras.models import load_model
from pickle import load
import numpy as np
from PIL import Image
# import matplotlib.pyplot as plt
import argparse



app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
token_nizer='model/'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL']=token_nizer
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])



# def extract_features(filename, model):
#         try:
#             image = Image.open(filename)
            
#         except ValueError:
#             print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
#         image = image.resize((299,299))
#         image = np.array(image)
#         # for images that has 4 channels, we convert them into 3 channels
#         # if image.shape[2] == 4: 
#         #     image = image[..., :3]
#         image = np.expand_dims(image, axis=0)
#         image = image/127.5
#         image = image - 1.0
#         feature = model.predict(image)
#         return feature
# def word_for_id(integer, tokenizer):
#  for word, index in tokenizer.word_index.items():
#      if index == integer:
#          return word
#  return None

# def generate_desc(model, tokenizer, photo, max_length):
    # in_text = 'start'
    # for i in range(max_length):
    #     sequence = tokenizer.texts_to_sequences([in_text])[0]
    #     sequence = pad_sequences([sequence], maxlen=max_length)
    #     pred = model.predict([photo,sequence], verbose=0)
    #     pred = np.argmax(pred)
    #     word = word_for_id(pred, tokenizer)
    #     if word is None:
    #         break
    #     in_text += ' ' + word
    #     if word == 'end':
    #         break
    # return in_text

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		img_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
		max_length = 32
		# tokenizer = os.path.join(app.config['MODEL'], filename)
		# model = os.path.join(app.config['MODEL'], filename)
		# xception_model = Xception(include_top=False, pooling="avg")

		# photo = extract_features(img_path, xception_model)
		# img = Image.open(img_path)

		# description = generate_desc(model, tokenizer, photo, max_length)
		# print("\n\n")
		# print(description)



		flash('Image successfully uploaded and displayed')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()