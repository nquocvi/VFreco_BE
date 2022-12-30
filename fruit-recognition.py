from flask import Flask, request, jsonify
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup
import werkzeug
import wikipedia

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "upload_images"

model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot', 7: 'cauliflower', 8: 'chilli pepper',9: 'coconut', 10: 'corn', 11: 'cucumber', 12: 'custard apple', 13: 'eggplant', 14: 'garlic', 15: 'ginger', 16: 'grapes', 17: 'guava', 18: 'jalepeno', 19: 'kiwi', 20: 'lemon', 21: 'lettuce',
          22: 'mango', 23: 'onion', 24: 'orange', 25: 'paprika', 26: 'pear', 27: 'peas', 28: 'persimmon', 29: 'pineapple', 30: 'pomegranate', 31: 'potato',32: 'pumkin', 33: 'raddish', 34: 'soy beans', 35: 'spinach', 36: 'sweetcorn', 37: 'sweetpotato', 38: 'tomato', 39: 'turnip', 40: 'watermelon', 41: 'wintermelon'}

fruits = ['Apple','Banana','Bello Pepper','Chilli Pepper','Custard Apple','Grapes','Jalepeno','Kiwi','Lemon','Mango','Orange','Paprika','Pear','Pineapple','Pomegranate','Watermelon','Wintermelon','Guava','Coconut','Pumkin','Persimmon']
vegetables = ['Beetroot','Cabbage','Capsicum','Carrot','Cauliflower','Corn','Cucumber','Eggplant','Ginger','Lettuce','Onion','Peas','Potato','Raddish','Soy Beans','Spinach','Sweetcorn','Sweetpotato','Tomato','Turnip']

def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        #st.error("Can't able to fetch the Calories")
        return "Can't able to fetch the Calories"
        print(e)

def fetch_content(prediction):
    try:
        return (wikipedia.summary(prediction))
        #return wikipedia.page(prediction).content
    except Exception as e:
        #st.error("Can't able to fetch the Calories")
        return "Can't able to fetch the Calories"
        print(e)


def processed_img(img_path):
    img=load_img(img_path,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'
    
@app.route("/upload-image", methods=["GET","POST"])
def run():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(image)

            filename = werkzeug.utils.secure_filename(image.filename)
            image.save("upload_images/" + filename)
            save_image_path =("upload_images/" + filename)

            with open(save_image_path, "wb") as f:
                f.write(image.getbuffer())                                  

            if image is not None:
                result= processed_img(save_image_path)
                status = "ok"
                if result in vegetables:
                    category = "Vegetable"
                else:
                    category = "Fruit"
                predicted = result
                cal = fetch_calories(result)
                con = fetch_content(result+' '+category)
                if(len(cal)>10):
                    calor = "Can't able to fetch the Calories"
                else: 
                    calor = (cal+'(100 grams)')
                print(cal)
                return jsonify({'status': status, 'category' : category, 'predicted' : predicted, 'calor':calor, 'con':con})
                print("ok")

    return  jsonify({'status' : "ok"})

if __name__ =="__main__":
    app.run(debug=True)