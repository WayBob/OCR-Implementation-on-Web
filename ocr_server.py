import json
import os
import cv2
import pytesseract
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify
from os import path
from werkzeug.utils import secure_filename
from ocr_test_local import cvt_b64_to_cv2
app = Flask(__name__)


def allowed_file(f_name):
    """
    Examine file type
    :param f_name: uploaded image file by client
    :return: True or False
    """
    return '.' in f_name and f_name.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'tif', 'tiff']


@app.route('/')
def welcome():
    """
    Welcome page
    :return: open the url(e.g., http://127.0.0.1:5000) to enter OCR HOMEPAGE
    """
    return render_template('welcome.html', message="Welcome~ here is the homepage for Bob's OCR!")


@app.route("/image-sync", methods=['GET', 'POST'])
def ocr():
    """
    Server END OCR process client requested b64-encoded image file
    :return: recognized text in .json
    """
    if request.method == 'POST':
        # receive the request from client
        upload_file = request.data.decode()
        # convert bytes into python-dict for post-process
        dict_file = json.loads(json.loads(upload_file))

        # Post-process Start then Employ OCR
        # acquire task id
        dict_file['task_id'] = dict_file['image_type'] + str(np.random.randint(0, 100))
        # background  processing start
        print('Start Processing File: \n',
              '########################### \n',
              'Task ID: {} \n'.format(dict_file['task_id']),
              'File Name: {} \n'.format(dict_file['name']),
              '########################### \n',)
        # read b64str image
        b64_str = dict_file['image_data']
        # convert encoded base64-string into image
        image = cvt_b64_to_cv2(b64_str)
        # employ tesseract to achieve OCR
        text = pytesseract.image_to_string(image)
        dict_file['ocr_text'] = text

        # save processed data
        save_path = os.path.join(os.getcwd(), 'cache', '{}.json'.format(dict_file['task_id']))
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(dict_file, indent=4, ensure_ascii=False))

        # return jsonify({'text': text, 'task_id': name})

        return jsonify({'Task_ID': dict_file['task_id']})

    if request.method == 'GET':

        task_id = request.get_json()['Task_ID']
        task_path = os.path.join(os.getcwd(), 'cache', '{}.json'.format(task_id))
        with open(task_path,'r', encoding='utf-8') as f:
            load_dict = json.load(f)
            OCR_out = load_dict['ocr_text']
        os.remove(task_path)
        return jsonify({'task_id': OCR_out})


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Web page for upload image then return OCR-processed text
    :return: recognized text in .json
    """
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        f = request.files['file']
        # return a secure version of filename
        filename = secure_filename(f.filename)
        if f and allowed_file(f.filename):
            save_path = os.path.join (os.getcwd(), 'cache')
            print(save_path)

        # save uploaded image into cache
        f.save(path.join(save_path, filename))
        img = cv2.imread(os.path.join(save_path, filename))
        print('Read Image File shape is : ', img.shape)
        # employ tesseract to achieve OCR
        ocr_output = pytesseract.image_to_string(img)
        print('OCR Recognized Output is : ', ocr_output)
        # delete client data in cache
        os.remove(os.path.join(save_path, filename))

        # return "{} successfully upload images！".format(f.filename)
        return jsonify({"text": ocr_output})


if __name__ == "__main__":

    app.run(debug=True)