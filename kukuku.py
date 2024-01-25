import subprocess
import os
import shutil
import zipfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

""" 스크립트 의도
1. 타겟 파일 입력
2. 파일 검사 시작
3. 파일에서 .dex 로 끝나는 파일은 모두 복호화 시도
4. 복호화 결과의 시작 부분이 dex로 시작한다면 정상 해독으로 간주하고 그 파일들만 저장
5. 저장된 파일 다시 repack
6. 정적, 동적 분석 실행 """

""" 사용법
1. pip install cryptography 설치 + mobsf 는 실행 중이어야 합니다.
2. file_analysis 함수에서 java apktool 명령어 수정 (버전정보, 파일 위치 정보)
3. start_analyse 함수에서 원하는 디렉토리와 타켓 수정 
4. kikiki.py에서 APIKey 수정 필요할 수도 있습니다."""

def decrypt_file(file_path): #암호문 해독
    key = b'dbcdcfghijklmaop' 
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    
    try:
        with open(file_path, 'rb') as encrypted_file: #파일 복호화
            encrypted_data = encrypted_file.read()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        if decrypted_data[:3].decode('utf-8', errors='ignore').startswith('dex'):  
            directory_path = os.path.dirname(file_path)
            classes2_path = os.path.join(directory_path, 'classes2.dex')
            classes3_path = os.path.join(directory_path, 'classes3.dex')
            
            save_path = classes3_path if os.path.exists(classes2_path) else classes2_path #클래스2있으면 3으로 저장 ㅋ.ㅋ..
            
            with open(save_path, 'wb') as dex_file: #파일 복호화 후 그 디렉터리에 저장
                dex_file.write(decrypted_data)
                print(f"Decrypted file saved as: {save_path}")
                return True

    except Exception as e: #예외나면 그냥 패스.
         pass  

def apk_to_zip(apk_file_path): 
    # APK 파일 이름과 확장자 분리
    base_name, extension = os.path.splitext(apk_file_path)
    
    # ZIP 파일 경로 생성
    zip_file_path = base_name + ".zip"
    
    # APK 파일을 ZIP 파일로 변환
    shutil.move(apk_file_path, zip_file_path)
    return zip_file_path


def file_analysis(target_path, target): #파일 분석
    print("Start analysing your target")
    os.chdir(target_path)
    subprocess.run(["java", "-jar", "apktool_2.9.2.jar", "d", "-f", "-s", target, "-o", "depack"], check=True) # 여기 수정해 주세요(버전, 명령어, 원하는 파일 이름)
    new_target_path = os.path.join(target_path, "depack") #원하는 파일 이름 달라졌으면 "depack도 수정해 주세요"
    for root, dirs, files in os.walk(new_target_path): #순환하면서 파일 찾기
            for file in files:
                file_path = os.path.join(root, file)
                if file == "kill-classes.dex" or file == "kill-classes2.dex":
                    decrypted_data = decrypt_file(file_path) # 복호화 함수로 토스
                elif file.endswith(".apk"): #만약 또 apk가 있으면 zip 파일로 전환 후 다시 압축해제하여 파일 탐색
                # APK 파일을 ZIP으로 변환
                    zip_file_path = apk_to_zip(file_path)
                    extracted_dir_path = os.path.splitext(zip_file_path)[0]
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall(extracted_dir_path)
                    os.remove(zip_file_path) # 알집 제거
                    for root, dirs, files in os.walk(extracted_dir_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if file == "kill-classes.dex" or file == "kill-classes2.dex":
                                decrypted_data = decrypt_file(file_path)
    
    subprocess.run(["java", "-jar", "apktool_2.9.2.jar", "b", "depack", "-o", "repack.apk"], check=True) #여기 수정해 주세요

# 분석 시작 -> 타켓 정하고 검사 -> 검사 끝나면 정적 동적 분석 정할거다.
def start_analyse(): 
        while True:
            try:
                print("please wait... we are checking your target")
                target_path = "D:/virous_sample/test"  #여기 수정해 주세요
                target =  "malware.apk.zip"              
                file_analysis(target_path, target)
                repacked_target = "repack.apk"
                print("ok. all done.")
                
                while True:
                    action = input ("Static analysis or Dynamic analysis? please enter (S/D): ") 

                    if action == "S":
                        import kikiki
                        kikiki.main(target_path, repacked_target)
                        print("Static analysis completed. What's next?")
                        continue
                    elif action == "D": # 동적은 몰라서 패스..
                        print("please enter dynamic code")
                        break
                    else:
                        print("Invalid input. Please enter S or D")
                        continue
                break

            except Exception as e:
                print("Error occurred: ", e)
                break
            
start_analyse()

