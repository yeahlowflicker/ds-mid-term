from flask import Flask, request, send_file, jsonify
from esrgan_model import RealESRGAN
from esrgan_anime_model import RealESRGAN_Anime
from classic_upscale import upscale_bicubic, upscale_lanczos, upscale_bicubic_sharpen
import os
import io

app = Flask(__name__)
anime_model = RealESRGAN_Anime(model_path='weights/RealESRGAN_x4plus_anime_6B.pth')

# GET / : endpoint to check if the server is running
@app.route('/')
def home():
    return jsonify({"message": "Real-ESRGAN backend is running!"}), 200

# POST /enhance : accepts the uploaded image and returns the enhanced version 
@app.route('/esrgan', methods=['POST'])
def enhance_esrgan():
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
        return jsonify({"error": str(e)}), 500
    
@app.route('/anime', methods=['POST'])
def enhance_anime():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    
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
        return jsonify({"error": str(e)}), 500

@app.route('/bicubic', methods=['POST'])
def enhance_bicubic():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        result = upscale_bicubic(image_file.read())

        return send_file(
            io.BytesIO(result),
            mimetype='image/png',
            as_attachment=False,
            download_name='enhanced_bicubic.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/lanczos', methods=['POST'])
def enhance_lanczos():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        result = upscale_lanczos(image_file.read())

        return send_file(
            io.BytesIO(result),
            mimetype='image/png',
            as_attachment=False,
            download_name='enhanced_lanczos.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sharpen', methods=['POST'])
def enhance_bicubic_sharpen():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        result = upscale_bicubic_sharpen(image_file.read())

        return send_file(
            io.BytesIO(result),
            mimetype='image/png',
            as_attachment=False,
            download_name='enhanced_sharpen.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=5000)