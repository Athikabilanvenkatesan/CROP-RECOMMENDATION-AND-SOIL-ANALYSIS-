import os
from rich.progress import track
import uuid
import flask
import urllib
import pickle
import pandas as pd
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'soil_analysis2.h5'))


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

classes = ['Black Soil','Laterite Soil','Red Soil','Saline Soil']


def predict(filename , model):
    img = load_img(filename , target_size = (220 , 220))
    img = img_to_array(img)
    img = img.reshape(220 ,220 ,3)
    img = np.expand_dims(img, axis = 0)
    img = np.vstack([img])


    result = model.predict(img)

    dict_result = {}
    for i in range(4):
        dict_result[result[0][i]] = classes[i]

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]
    
    prob_result = []
    class_result = []
    for i in range(1):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])

    return class_result , prob_result




@app.route('/')
def home():
        return render_template("home.html")

@app.route('/crop')
def crop():
       return render_template('home.html')


@app.route('/soil')
def soil():
      return render_template('soil.html')

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static/images')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img , filename)
                output = open(img_path , "wb")
                output.write(resource.read())
                output.close()
                img = filename

                class_result , prob_result = predict(img_path , model)

                predictions = {
                      "class1":class_result[0],
                        
                        "prob1": prob_result[0],
                        
                }

            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('soil.html' , error = error) 

            
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                class_result , prob_result = predict(img_path , model)

                predictions = {
                      "class1":class_result[0],
                        
                        "prob1": prob_result[0],
                        
                }

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('soil.html' , error = error)

    else:
        return render_template('soil.html')

global loaded_model
loaded_model = pickle.load(open("yieldfinal.pkl", "rb"))
# prediction function
def ValuePredictor(to_predict_list):
	to_predict = np.array(to_predict_list).reshape(1, 6)
	
	result = loaded_model.predict(to_predict)
	return result[0]

@app.route('/result', methods = ['POST'])
def result():
	if request.method == 'POST':
            state = int(request.form['state'])
            district = int(request.form['district'])
            seasons = int(request.form['seasons'])
            year = int(request.form['year'])
            crops = int(request.form['crops'])
            area = int(request.form['area'])
            y_pred = [[state,district,seasons,year,crops,area]]

            result1 = ValuePredictor(y_pred)
            data = pd.read_csv("crop.csv")
            result2=[]
            for i in track(range(1,len(data))):
              crop = data["Crop_v"][i]
              y_pred2 = [[state,district,seasons,year,crop,area]]
              result2.append(loaded_model.predict(y_pred2))

            for i in range(len(result2)):
              if(result2[i]== max(result2)):
                a = data['Crop'][i]
            if(result1 == max(result2)):
                
                recommendation = "your crop gives more production of {}".format(result)
            else:
                recommendation = "{} gives more production of {} and your selected crop gives production of {}".format(a,int(max(result2)),int(result1))


            
                            
            return render_template("home.html",recommendation = recommendation)





if __name__ == "__main__":
    app.run(debug = True)


