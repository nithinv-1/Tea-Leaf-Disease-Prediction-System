import os
import cv2

import numpy as np
import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# For prediction using our trained model
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

import json
import sys
import serial

filepath = '../public/tea.hdf5'
model = load_model(filepath)
#print("Model Loaded Successfully")

test_img_path=sys.argv[1]
test_image = load_img(test_img_path, target_size=(180,180))  # Load image 
test_image = img_to_array(test_image)  # Convert image to numpy array
test_image = np.expand_dims(test_image, axis=0)  # Change dimension from 3D to 4D
result = model.predict(test_image)  # Predict disease
pred = np.argmax(result, axis=1)[0]
expression = ['Anthracnose', 'algal leaf', 'bird eye spot', 'brown blight', 'gray light', 'healthy', 'red leaf spot', 'white spot']
test_image = plt.imread(test_img_path)
#print(expression[pred])
r=expression[pred]
#plt.imshow(test_image)
#sav_loc='../public/output/'+r+'.png'
#plt.savefig(sav_loc, bbox_inches="tight", pad_inches=0)

try:
    arduino = serial.Serial("COM5", timeout=10, baudrate=9600)

    turn = 3
    while (turn > 0):
        try:
            strstr = str(arduino.readline())
            t = 0
            humi = ""
            temp = ""
            moist = ""
            for i in range(len(strstr)):
                if strstr[i] == "r":
                    break
                if strstr[i] == "'":
                    t = 1
                    continue
                if strstr[i] == ";":
                    if t == 1:
                        t = 2
                    else:
                        t = 3
                    continue
                if t == 1:
                    humi += strstr[i]
                elif t == 2:
                    temp += strstr[i]
                elif t == 3:
                    moist += strstr[i]

            print("humidity :", humi)
            print("temperature :", temp)
            print("moisture :", moist[0:-1])
            turn -= 1
        except KeyboardInterrupt:
            break
    
    if (float(moist[0:-1])<1100 and float(moist[0:-1])>=600):
        sugest='Soil is very Dry'
        fsuggest="Turn on Irrigation System"
        if(float(temp)<16):
            sugest=sugest+", Temperature is very Low"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        elif(float(temp)>=16 and float(temp)<=32):
            sugest=sugest+", Temperature is Ideal"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        elif(float(temp)>32):
            sugest=sugest+", Temparature is High"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        else:
            sugest=sugest+", ERROR"
        

    elif (float(moist[0:-1])<600 and float(moist[0:-1])>=470):
        sugest='Ideal Soil Moisture'
        fsuggest="Controlled Irrigation"
        if(float(temp)<16):
            sugest=sugest+", Temperature is very Low"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        elif(float(temp)>=16 and float(temp)<=32):
            sugest=sugest+", Temperature is Ideal"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        elif(float(temp)>32):
            sugest=sugest+", Temparature is High"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        else:
            sugest=sugest+", ERROR"


    elif (float(moist[0:-1])<470):
        sugest='Soil is very wet'
        fsuggest="Stop Irrigation System"
        if(float(temp)<16):
            sugest=sugest+", Temperature is very Low"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        elif(float(temp)>=16 and float(temp)<=32):
            sugest=sugest+", Temperature is Ideal"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        elif(float(temp)>32):
            sugest=sugest+", Temparature is High"
            if(float(humi)<95 and float(humi)>60):
                sugest=sugest+", Suitable Humidity"
            elif(float(humi)<=60):
                sugest=sugest+", Low Air Humidity"
            else:
                sugest=sugest+", ERROR"


        else:
            sugest=sugest+", ERROR"


    else:
        sugest='ERROR'
    

    #ferti="Fertilizer"

    #fsuggest="* EDIT *"
    if(r=="Anthracnose"):
        ferti="To control "+r+", Spray with Anti-Microbial Biopesticides such as Mildew or Biostimul in appropriate dosage. Reduce watering and prune the bushes. Air and sunlight prevents the spread of anthracnose naturally. Space your plants far enough apart for better air circulation and help more sunlight to reach the plants. "
    elif(r=="algal leaf"):
        ferti="To control "+r+", Remove and destroy the infected portion by spraying of bordeaux mixture. Improve soil drainage by tilling and add NPK fertilizer depending on the area requirement."
    elif(r=="brown blight" or r=="gray light"):
        ferti="To control "+r+", Prune the affected leaves and Spray Copper oxychloride at 5-7 days interval until new buds bloom. Increase the time of irrigation for improved soil moisture holding. Plants with adequate spacing permit more direct sunrays and improve leaf health."
    elif(r=="red leaf spot" or r=="bird eye spot"):
        ferti=r+" appears first as dark red or brown spots caused by a warm and wet weather and badly drained soil. Use Copper Oxychloride 0.2 or Mancozeb 0.25 to reduce the spread and remove the infected twigs. Improve Soil Drainage and use nutrient mixed water for irrigation."
    elif(r=="white spot"):
        ferti="To control "+r+", Prune the plants and Spray Copper oxychloride, NiCl2 mixture (420 g/ha) at 5 days interval until new buds bloom. Improve spacing between plants to improve air circulation and reduce humidity and the duration of leaf wetness."
    elif(r=="healthy"):
        ferti="Leaf is healthy. Continue Regular Farming Practice and monitor leaf periodically for easy prevention and control measures. "
    else:
        ferti="error"
    

    result = {
        "loc" : sys.argv[1].split("\\")[-1],
        "disease": r,
        "humidity": humi+" %",
        #"Humdity_result":Humidity_statement,
        "temperature": temp+" °C",
        "moisture": moist[0:-1],
        "suggestion":sugest,
        "farmingsuggestion":fsuggest,
        "fertilizersuggest":ferti
    }

    print(json.dumps(result))

except Exception as e:
    print('Error occurred:', e)
    
r='''result = {
        "disease" : r,
        "humidity" : "100",
        "temperature ": "200",  
        "moisture " : "300"
}

print(json.dumps(result))'''