import mlflow 
import uvicorn
import json
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile



print(mlflow.__version__)

description = """
API description 
# Just try it 
"""

tags_metadata = [
    {
        "name": "tag_1",
        "description": "description"
    },
    {
        "name": "tag_2",
        "description": "description"
    }
]

class Input(BaseModel):
    input: list

dataset = pd.read_excel('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/ibm_hr_attrition.xlsx')

app = FastAPI(
    title="🚗 Getaround prediction Api",
    description=description,
    version="0.1",
    contact={
        "name": "Aon",
        "url": "http://none.com",
    },
    openapi_tags=tags_metadata
)

mlflow.set_tracking_uri("https://mlflow-s3-5c46c0d9d46b.herokuapp.com/")
logged_model = 'runs:/18f2bcb978c2417cb3c6f85174da829e/xgboost'
#logged_model = 'pricing_modeling/logged_model/getaround_price_prediction'
print('loading model...')
loaded_model = mlflow.pyfunc.load_model(logged_model)
print('...model loaded')


@app.post("/predict", tags=["tag_1"])
async def index(input:Input):
    print(input)
    # Read data 
    columns = ['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color',
       'car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect',
       'has_speed_regulator', 'winter_tires']
    features = pd.DataFrame([input.input], columns=columns)
    features['private_parking_available'].astype(bool)
    features['has_gps'].astype(bool)
    features['has_air_conditioning'].astype(bool)
    features['automatic_car'].astype(bool)
    features['has_getaround_connect'].astype(bool)
    features['has_speed_regulator'].astype(bool)
    features['winter_tires'].astype(bool)
    print('features_type',type(features))
    print(features)

    # Run prediction
    prediction = loaded_model.predict(features)
    print('prediction',prediction)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

@app.post("/batch-predict", tags=["tag_1"])
async def batch_pred(file: UploadFile = File(...)):
    """
    Make batch predictions 
    
    """
    df = pd.read_csv(file.file)

    # Run prediction
    prediction = loaded_model.predict(df)
    print('predictions', prediction)

    # Format responses
    response = {"prediction": prediction.tolist()}

    return response
    

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)