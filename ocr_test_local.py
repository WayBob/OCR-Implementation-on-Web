import argparse
import json
import cv2
import numpy as np
import base64
import requests

# convert cv2 into base64
def cvt_cv2_to_b64(image):
    """
    Convert image read by opencv into base64
    :param image: cv2 read img
    :return: base64 string of img
    """
    base64_str = cv2.imencode('.tif', image)[1].tostring()
    image_b64 = base64.b64encode(base64_str)
    image_str = image_b64.decode()
    return image_str

# convert base64 into cv2
def cvt_b64_to_cv2(b64_str):
    """
    Convert base64 image into cv2 readable
    :param b64_str: base64 string of img
    :return: cv2 readable img
    """
    imgString = base64.b64decode(b64_str)
    nparr = np.fromstring(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def main(url, ori_path, headers):
    """
    This is client END request for a image-to-text OCR based on tesseract
    :param url: server END http address.
    :param ori_path: client's local image file path.
    :return:text file of the recognition result of OCR.
    """
    # read .tif images
    img = cv2.imread(ori_path, 0)
    filename = ori_path.rsplit('/', 1)[1]
    filetype = filename.rsplit('.', 1)[1]
    print('file.name: ', filename)
    # print size of image
    print('file.size: ', img.shape)
    # print file type of image
    print('file.type: ', filetype)
    # convert image into b64
    b64str = cvt_cv2_to_b64(image=img)

    # prepare json file
    file_js = {}
    file_js['image_data'] = b64str
    file_js['shape'] = img.shape
    file_js['name'] = filename
    file_js['image_type'] = filetype

    print('Uploading client image: {}'.format(file_js['name']))

    # Generate Task-ID output
    response = requests.post(
        url=url,
        headers=headers,
        json=json.dumps(file_js, indent=4, ensure_ascii=False)
    )
    print(response)
    results = json.loads(response.text)
    print('Your OCR task has been uploaded sucessfully, '
          'please receive and keep your task_ID:\n', results['Task_ID'])

    while(True):

        # Use Task-ID
        retrieve_id = input('Please input your Task_ID to retrieve OCR text: \n')
        id_js = {}
        id_js['Task_ID'] = retrieve_id
        if id_js['Task_ID'] == results['Task_ID']:
            print('Your Id {} is confirmed, please waiting for output. \n'.format(id_js['Task_ID']))
            response = requests.get(url=url, json=id_js)
            res = json.loads(response.text)
            print('The OCR recognized text output is shown as follows:',
                  '\n################\n',
                  res['task_id'],
                  '\n################')
            break
        else:
            print('Sorry,the input task ID is wrong, please confirm and try it again.')
            continue


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default='http://127.0.0.1:5000/image-sync',
                        help='url for tesseract based ocr')
    parser.add_argument('--headers', type=dict, default={"Content-type": "application/json", "Accept": "text/plain", "charset": "UTF-8"},
                        help='header file')
    parser.add_argument('--data', type=str, default='./phototest.tif',
                        help='original image path')
    opt = parser.parse_args()
    main(opt.url, opt.data, opt.headers)


