# MOBILESANEBOXCODE  

### MOBSF 셋팅
1.. Android studio & app tools, 지니모션, 파이썬 3.10 버전,openssl,JDK(11),visual studio build-tools 설치  
2. SAMPLE.APK를 기준으로 에뮬레이터는 안드로이드 9버전으로 설정할것  
3. Custom API Documentation 문서에 있는 구글드라이브 링크를 열어 그 안에 있는 압축파일을 풀고 주소창에 cmd라 입력하면 나오는 커맨드라인창에  run poetry , setup.bat, run.bat을 입력한다.   
4. 설치가 제대로 되었는지 확인하기 위해 인터넷 브라우저를 킨다음에 주소창에 127.0.0.1:8000이라 입력한다.  
5. 앱을 드래그 앤 드롭을 해본다  
6. 동적분석이 되지 않으면 https://github.com/m9rco/Genymotion_ARM_Translation/blob/master/package/Genymotion-ARM-Translation_for_9.0.zip 이 사이트에서 Genymotion-ARM-Translation_for_9.0.zip을 다운 받아 켜진 에뮬레이터에 드래그앤 드랍 후 다시 시도할것  


### preprocessing.py 사용법  
1. 폴더를 생성후 폴더안에 암호화를 해제할 필요가 있는 apk 파일 1개와 apktool.jar 파일을 집어 넣습니다.  
2. 폴더를 만들때 폴더 이름에 빈칸과 한글을 포함하지 않은 단어로 생성하세요. 코드 검증 과정중에 폴더 이름에 빈칸이 있을때 오류가 발생하였던 경우가 있습니다.
3. 코드를 동작시키면 폴더 내부에 있는 apk 파일이 자동으로 선정되고 APK파일 내부에서 암호화를 해제할 파일명을 지정한 다음에 암호화 해제 방식과 키를 입력하면 암호화 해제하고 덮어씌운 파일이 포함되고 자동으로 사인이 생성된 app-signed.apk 파일이 만들어집니다  

### analysis.py 사용법  
1. analysis.py의 APIKEY를 본인의 APIKEY에 맞게 변경
2. Mobile-Security-Framework-MobSF-master가 설치된 폴더를 열고 그 주소창에 cmd라 입력하면 명령 프롬포트 창에 run.bat이라 입력한다.
3. 웹 페이지를 열고 127.0.0.1:8000이라 입력한다.
4. 지니에뮬레이터를 켠다.
5. analysis.py를 실행후에 암호화 해제하지 않은 apk파일경로입력  

### 기능  
1. 정적 분석  
2. 동적 분석  
3. 내부 APK 분석  
4. 정적 분석 PDF 파일([HASH].pdf) 생성  

### 시현 동영상
[![analysis](http://img.youtube.com/vi/OT9e2_psQKk/0.jpg)](https://youtu.be/OT9e2_psQKk)
