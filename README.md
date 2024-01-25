# MOBILESANEBOXCODE  


###preprocessing.py 사용법  
폴더를 생성후 폴더안에 apk 파일 1개와 apktool.jar 파일을 집어 넣습니다.  
폴더를 만들때 폴더 이름에 빈칸과 한글을 포함하지 않은 단어로 생성하세요. 코드 검증 과정중에 폴더 이름에 빈칸이 있을때 오류가 발생하였던 경우가 있습니다.  
코드를 동작시키면 폴더 내부에 있는 apk 파일이 자동으로 선정되고 폴더 내부에 있는 파일명을 지정한 다음에 암호화 해제 방식과 키를 입력하면 자동으로 사인이 생성된 app-signed.apk 파일이 만들어집니다  

### analysis.py 사용법  
1. analysis.py의 APIKEY를 본인의 APIKEY에 맞게 변경  
2. Custom API Documentation 문서에 있는 구글드라이브 링크를 열어 그 안에 있는 압축파일을 풀고 주소창에 cmd라 입력하면 나오는 커맨드라인창에  run poetry , setup.bat, run.bat을 입력한다.    
3. analysis.py를 실행후에 파일경로입력  

### 기능  
1. 정적 분석  
2. 동적 분석  
3. 내부 APK 분석  
4. 정적 분석 PDF 파일([HASH].pdf) 생성  

