# coding=utf-8
import json

from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from api.util import *

from algorithm.scene_labeling import serve

# Create a Blueprint for the nas API
nas_api = Blueprint('nas_api', __name__)

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@nas_api.route('/nas/api/scene-recognition', methods=['POST'])
def scene_recognition():
    print request
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Secure the filename and save it
        filename = secure_filename(file.filename)
        img_file_pth = os.path.join(UPLOAD_FOLDER, filename)
        file.save(img_file_pth)

        try:
            top_k_recognition_result, cost_time = serve(img_file_pth)
        except Exception as e:
            return jsonify({'error': "Algorithm fail", 'msg': str(e)}), 500

        return jsonify({
            'uploaded_file': filename,
            'top_k_results': top_k_recognition_result,
            'cost_time': cost_time
        }), 200

    return jsonify({'error': 'Invalid file type'}), 400

@nas_api.route('/nas/api/alert_test', methods=['GET'])
def alert_test():
    feishu_bot_send_text(123456)
    feishu_bot_send_rich_text("题目", "内容", "https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN#f62e72d5")
    return jsonify({'success': True}), 200

