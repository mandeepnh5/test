import azure.functions as func
import cv2
import numpy as np
from io import BytesIO
import json
import base64
from PIL import Image

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get the request body as JSON
        req_body = req.get_json()
        
        # Get base64 string from JSON
        if 'image' not in req_body:
            return func.HttpResponse(
                "Please pass an 'image' field in the request body",
                status_code=400
            )
            
        base64_image = req_body['image']
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_image)
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Convert back to PIL Image
        pil_image = Image.fromarray(gray_image)
        
        # Convert processed image to base64
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        processed_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Return JSON response with base64 image
        return func.HttpResponse(
            body=json.dumps({
                "processed_image": processed_image_base64
            }),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        return func.HttpResponse(
            body=json.dumps({
                "error": str(e)
            }),
            mimetype="application/json",
            status_code=500
        )