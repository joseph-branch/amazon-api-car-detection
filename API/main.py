from typing import Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

app.car_count = 0

@app.get("/car-count", status_code = 200)
async def getCarCount():
    print(app.car_count)
    
    json_compatible_data = jsonable_encoder(app.car_count)
    return JSONResponse(content = json_compatible_data)

@app.post("/car-count/{cars}", status_code = 200)
async def setCarCount(cars: int):
    print(f"cars {cars}")
    app.car_count = cars
    return
