import os
import ast
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

SERVER = "http://127.0.0.1:8000"
APIKey = 'fc61093d07e6295b02ec4670ec34639fbad87bfc7fd6daa38d1b2b8acc4023ca' 

def upload(file):
    file_name = file.split('\\')[-1]
    multipart_data = MultipartEncoder(fields={'file': (file_name, open(file, 'rb'), 'application/octet-stream')})
    headers = {'Content-Type': multipart_data.content_type, 'Authorization': APIKey}
    response = requests.post(SERVER + '/api/v1/upload', data=multipart_data, headers=headers)
    print(response.text)
    return response.text # 출력값 다른 곳에서 활용


def scan(data):
    post_dict = json.loads(data)
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/scan', data=post_dict, headers=headers)
    return r.text

def pdf(data):
    data = {"hash" : json.loads(data)['hash']}
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/download_pdf', data=data, headers=headers)
    path = ".\\" + data['hash'] + '.pdf'
    with open(path, 'wb') as word : 
        print(r)
        for chunk in r.iter_content(chunk_size = 8192):
            if chunk:
                word.write(chunk)
        return path

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

def scan_nested_apk(data):
    """Scan the Nested apk"""
    print("Scanning file")
    post_dict = json.loads(data)
    headers = {'Authorization': APIKey}
    response = requests.post(SERVER + '/api/v1/find_nested_apk', data=post_dict, headers=headers)
    return response.text

# Dynamic
def get_app():
    headers = {'Authorization': APIKey}
    response = requests.post(SERVER + '/api/v1/dynamic/get_apps', headers=headers)
    return response.text

def dynamic_json_pdf(data):
    post_dict = {'hash' : json.loads(data)['hash']}
    headers = {'Authorization': APIKey}
    response = requests.post(SERVER + '/api/v1/dynamic/report_json',  data=post_dict, headers=headers)
    return response.text

def start_dynamic(data):
    post_dict = {'hash' : json.loads(data)['hash']}
    headers = {'Authorization': APIKey}
    response = requests.post(SERVER + '/api/v1/dynamic/start_analysis',  data=post_dict, headers=headers)
    return response.text

def stop_dynamic(data):
    post_dict = {'hash' : json.loads(data)['hash']}
    headers = {'Authorization': APIKey}
    
    response = requests.post(SERVER + '/api/v1/dynamic/stop_analysis',  data=post_dict, headers=headers)
    return response.text

def frida_instrument(data):
    post_dict = {'hash' : json.loads(data)['hash']}
    frida_code = ''
    
    # apk 별 frida 코드 설정
    if post_dict['hash'] == 'f90f81f7b47ca73de0e5aa5aaeba6735':
        frida_code = """
        Java.perform(function() {
        var CheckClass = Java.use("com.ldjSxw.heBbQd.a.b");
        
        CheckClass.k.implementation = function(context){
            return false;
        };
        });
        """
    
    post_dict['default_hooks'] = ['api_monitor','ssl_pinning_bypass','root_bypass','debugger_check_bypass']
    post_dict['auxiliary_hooks'] = ''
    post_dict['frida_code'] = frida_code
    headers = {'Authorization': APIKey}
    
    response = requests.post(SERVER + '/api/v1/frida/instrument',  data=post_dict, headers=headers)
    return response.text

def activity(data):
    post_dict = {'hash' : json.loads(data)['hash']}
    post_dict['test'] = 'activity' # exported or activity
    headers = {'Authorization': APIKey}
    
    response = requests.post(SERVER + '/api/v1/android/activity',  data=post_dict, headers=headers)
    return response.text

def recu_scan(data):
    apps = []
    nested_list = scan_nested_apk(data)
    nested_list = ast.literal_eval(nested_list)
    apps_num = len(nested_list)
    if apps_num > 0:
        for i in range(apps_num):
            apps.append(nested_list[str(i)])
            app = recu_scan(nested_list[str(i)])
            if app:
                apps.extend(app)
        return apps
    else:
        return False
    

def analysis_start(RESP):
    scan(RESP)
    start_dynamic(RESP)
    frida_instrument(RESP)
    activity(RESP)
    stop_dynamic(RESP)
    pdf(RESP)

def main(file):
    RESP = upload(file)

    apps = [RESP]
    apps.extend(recu_scan(RESP))
    
    for app in apps:
        analysis_start(app)

if __name__ == "__main__":
    file = input('FILE PATH : ')
    main(file)
