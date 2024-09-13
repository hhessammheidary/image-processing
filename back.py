from flask import Flask, request, jsonify
import base64
from io import BytesIO 
import cv2 
from keras.models import load_model 
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:  
        model = load_model('C:/Users/HP/OneDrive/Desktop/ML/model/final_cnn.h5')
        # Get the image file from the request
        image_data = request.files['image'].read()
        
        # Decode the image data
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Convert the image data to a PIL Image
        # image = cv2.imread(BytesIO(decoded_image))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        image = cv2.resize(image, (100, 100))
        result = model.predict(image.reshape(1, 100, 100))
        names = ['AliDaei','AlirezaBeiranvand','BaharehKianAfshar','BahramRadan','HomayoonShajarian','JavadRazavian',
 'MehranGhafoorian','MohamadEsfehani','MohsenChavoshi','NazaninBayati','RezaAttaran','SaharDolatshahi','SeyedJalalHosseini',
 'SogolKhaligh', 'TaranehAlidoosti']  
        #result_text = names[result.argmax(axis=1)[0]] 
        # Create a JSON response
        response_data = {'result': "result_text"}

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
