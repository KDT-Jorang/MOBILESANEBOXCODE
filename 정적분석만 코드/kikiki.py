import os
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder



SERVER = "http://127.0.0.1:8000"
APIKey = '761d4877a14fb0f3e9f8df016c3b666ed5ca0847a5d616dd2e07ad88976ac9f3' #여기 수정해 주세요

def upload(target_path, target):
    print('start_file_analysing')
    full_target_path = os.path.join(target_path, target)
    multipart_data = MultipartEncoder(fields={'file': (target, open(full_target_path, 'rb'), 'application/octet-stream')})
    headers = {'Content-Type': multipart_data.content_type, 'Authorization': APIKey}
    response = requests.post(SERVER + '/api/v1/upload', data=multipart_data, headers=headers)
    print(response.text)
    return response.text # 출력값 다른 곳에서 활용
    #requests 인자 : url, data, json, headers, cookies는 dict 형태로, 
    # files : 'file' : (target, open(target, 'rb') 처럼
    # url 을 제외하고는 나머지는 필수가 아니다. 

def scan(data):
    print("스캐닝!!! 슈우우웅!")
    post_dict = json.loads(data)
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/scan', data=post_dict, headers=headers)
    print(r.text)

def pdf(data):
    data = {"hash" : json.loads(data)['hash']}
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/download_pdf', data=data, headers=headers, stream=True)
    with open('D:\\virous_sample\\test\\report_file.pdf', 'wb') as word :
        for chunk in r.iter_content(chunk_size = 8192):
            if chunk:
                word.write(chunk)
        return 'D:\\virous_sample\\test\\report_file.pdf'       

def json_pdf(data):
    data = {'hash' : json.loads(data)['hash']}
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/report_json', data=data, headers=headers)
    print(r.text)


def delete_scan(data):
    post_dict = {'hash' : json.loads(data)['hash']}
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/delete_scan', data=post_dict, headers=headers)
    print(r.text)



def main(target_path, target):
    RESP = upload(target_path, target)
    scan(RESP)
    pdf(RESP)
    json_pdf(RESP)
    delete_scan(RESP)

if __name__ == "__main__":
    target_path = input("Please enter the target path: ")
    target = input("Please enter the target file name: ")
    main(target_path, target)
