from flask import Flask, request, send_file, jsonify
from realesrgan import RealESRGANer
# from esrgan_model import RealESRGAN
from esrgan_anime_model import RealESRGAN_Anime
from classic_upscale import upscale_bicubic, upscale_lanczos, upscale_bicubic_sharpen
from sobel import enhance_quality_with_sobel
import os
import io
import json
from flask_sock import Sock
import base64
import numpy as np
import cv2

app = Flask(__name__)
sock = Sock(app) # Websocket instance

# anime_model = RealESRGAN_Anime(model_path='weights/RealESRGAN_x4plus_anime_6B.pth')

# GET / : endpoint to check if the server is running
@app.route('/')
def home():
    return jsonify({"message": "Real-ESRGAN backend is running!"}), 200

# POST /enhance : accepts the uploaded image and returns the enhanced version 
@app.route('/esrgan', methods=['POST'])
def enhance_esrgan():
    print('ESRGAN')
    
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    esrgan_model = RealESRGAN(model_path='weights/RealESRGAN_x4plus.pth')
    image_file = request.files['image']
    original_filename = os.path.splitext(image_file.filename)[0]
    try:
        result = esrgan_model.enhance(image_file.read())
        esrgan_filename = f"enhanced_esrgan_{original_filename}.png"
        return send_file(
            io.BytesIO(result),
            mimetype='image/png',
            as_attachment=False,
            download_name=esrgan_filename
        )
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/anime', methods=['POST'])
def enhance_anime():
    print('Anime')

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    anime_model = RealESRGAN_Anime(model_path='weights/RealESRGAN_x4plus_anime_6B.pth')
    image_file = request.files['image']
    original_filename = os.path.splitext(image_file.filename)[0]
    try:
        result = anime_model.enhance(image_file.read())
        anime_filename = f"enhanced_esrgan_anime_{original_filename}.png"
        return send_file(
            io.BytesIO(result),
            mimetype='image/png',
            as_attachment=False,
            download_name=anime_filename
        )
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



@sock.route('/ws')
def websocket(ws):
    print("Client connected via WebSocket.")
    while True:
        message = ws.receive()
        if message is None:  # Client disconnected.
            print("Client disconnected.")
            break

        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            error_response = {"error": "Invalid JSON", "details": str(e)}
            ws.send(json.dumps(error_response))
            continue

        uuid = data.get("uuid")
        enhancement_type = data.get("enhancement_type")
        image_data = data.get("image")

        if uuid is None or image_data is None:
            error_response = {"error": "Missing uuid or image data"}
            ws.send(json.dumps(error_response))
            continue

        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        print('Enhancement starting...')
        
        if enhancement_type == 'sobel':
            result = enhance_quality_with_sobel(image_bytes)
        elif enhancement_type == 'esrgan':
            pass
        elif enhancement_type == 'anime':
            pass
        elif enhancement_type == 'bicubic':
            result = upscale_bicubic(image_bytes)
        elif enhancement_type == 'lanczos':
            result = upscale_lanczos(image_bytes)
        elif enhancement_type == 'sharpen':
            result = upscale_sharpen(image_bytes)
        else:
            print('Invalid enhancement type. Aborting...')
            return

        print('Enhancement complete.')
            
        response = {
            "status": "success",
            "uuid": uuid,
            "result": base64.b64encode(result).decode()
        }

        ws.send(json.dumps(response))
    return

    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=5000)