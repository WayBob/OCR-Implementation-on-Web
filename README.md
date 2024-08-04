> This is a OCR (Optical Character Recognition) implement based on Tesseract from Google.  
> In particular, this work is done by Yubo (Bob) WANG for his application interests  

![OCR](static/images/Tesseract_logo_001.png)

## 1. OCR Request Example from Terminal  
### Implementation Process  
#### Step#1. Run the following in your terminal to Start Server (Server End)
```commandline
cd OCR_YuboWANG
pip3 install --upgrade pip
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 ocr_server.py 
```
Once successfully starting server, you will return the Running URL, e.g., `http://127.0.0.1:5000`
#### Step#2. Open another terminal for OCR test (User End)
```commandline
cd OCR_YuboWANG
python3 ocr_test_local.py
```
#### Step#3. Supplemental details for Step#2
```commandline
# 1. The default parameters could be checked&modified in path `OCR_YuboWANG/ocr_test_local.py` (Line94 to Line99).
# 2. In particualr, the test file is in path 'OCR_YuboWANG/phototest.tif'. The file will be uploaded via 'POST'.
# 3. The server will return a Task_ID consist of 'Image.type'+'numpp.randint(0, 100)', e.g., tif77
# 4. Please input the returned Task_ID in terminal to Get the OCR output
```

### Explanation
Method：`POST`、`GET`  
Server URL： `http://127.0.0.1:5000/image-sync`  
Default Test_image: ```OCR_YuboWANG/phototest.tif```

## 2. OCR Request Example from web

### Usage  
#### Step#1. Similarly, Run the following in terminal to Start Server (Server End)
```commandline
cd OCR_YuboWANG
pip3 install --upgrade pip
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 ocr_server.py 
```
Once successfully starting server, you will return the Running URL, e.g., Once successfully starting server, you will return the Running URL, e.g., `http://127.0.0.1:5000`  
#### Step#2. Open website and upload image file
```commandline
# 1. Open the server homepage, i.e., `http://127.0.0.1:5000`;
# 2. Click 'here' button jump to upload page, or you could direct access `http://127.0.0.1:5000/upload`;
# 3. Choose file from local then Click 'File Upload' button to upload image-file to server;
# 4. Obtain the returned OCR output.
```


