from typing import Union
import cv2 as cv
import numpy as np

from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        np_array = np.frombuffer(data, np.uint8)

        # tu obróbka
        img = cv.imdecode(np_array, cv.IMREAD_COLOR)
        img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        _, img_grey_bytes = cv.imencode('.jpg', img_grey)
        await websocket.send_bytes(img_grey_bytes.tobytes()) 