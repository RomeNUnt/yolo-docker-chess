from fastapi import FastAPI, UploadFile
from ultralytics import YOLO
import numpy as np
import cv2

app = FastAPI()

# Load your trained chess model
model = YOLO("chess_pieces.pt", task="detect")

@app.post("/predict")

async def predict(file: UploadFile):
    image_bytes = await file.read()

    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    print(type(img))
    print(img.size if hasattr(img, "size") else img.shape)

    results = model.predict(img)

    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox": {
                    "x1": float(box.xyxy[0][0]),
                    "y1": float(box.xyxy[0][1]),
                    "x2": float(box.xyxy[0][2]),
                    "y2": float(box.xyxy[0][3]),
                }
            })

    return {"detections": detections}
