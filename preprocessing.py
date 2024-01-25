import os
import subprocess
from Crypto.Cipher import AES


def decrypt_aes_ecb(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()

    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_data = cipher.decrypt(data)

    with open(file_path, "wb") as f:
        f.write(decrypted_data)


script_dir = os.path.dirname(os.path.realpath(__file__))
apktool_path = os.path.join(script_dir, "apktool.jar")

apk_path = None
for file in os.listdir(script_dir):
    if file.endswith(".apk"):
        apk_path = os.path.join(script_dir, file)
        break

if apk_path is None:
    print("현재 디렉토리에 APK 파일이 없습니다.")
    exit()

subprocess.run(
    [
        "java",
        "-jar",
        apktool_path,
        "d",
        "-s",
        apk_path,
        "-o",
        os.path.join(script_dir, "decompiled"),
    ]
)

decompiled_dir = os.path.join(script_dir, "decompiled")
encrypted_file_name = input("난독화된 파일의 이름을 입력해주세요: ")
encrypted_file_path = os.path.join(decompiled_dir, encrypted_file_name)
decryption_method = input("암호화 해제 방식을 입력해주세요 (예: AES-128/ECB): ")
decryption_key = input("암호화 해제 키를 입력해주세요: ")

if decryption_method == "AES-128/ECB":
    decrypt_aes_ecb(encrypted_file_path, decryption_key)
else:
    print(f"{decryption_method}는 지원하지 않는 암호화 해제 방식입니다.")

subprocess.run(
    [
        "java",
        "-jar",
        apktool_path,
        "b",
        decompiled_dir,
        "-o",
        os.path.join(script_dir, "decryption.apk"),
    ]
)

keystore_file = os.path.join(script_dir, "my-release-key.keystore")
alias_name = "alias_name"

keystore_password = "000000"

if not os.path.exists(keystore_file):
    keytool_command = [
        "keytool",
        "-genkey",
        "-v",
        "-keystore",
        keystore_file,
        "-alias",
        alias_name,
        "-keyalg",
        "RSA",
        "-keysize",
        "2048",
        "-validity",
        "10000",
        "-storepass",
        keystore_password,
        "-dname",
        "CN=j, OU=k, O=k, L=k, ST=j, C=082",
    ]
    subprocess.run(keytool_command)
else:
    print("Keystore file already exists. Skipping key generation.")

apk_file = os.path.join(script_dir, "decryption.apk")
signed_apk_file = os.path.join(script_dir, "app-signed.apk")
jarsigner_command = [
    "jarsigner",
    "-verbose",
    "-sigalg",
    "SHA1withRSA",
    "-digestalg",
    "SHA1",
    "-keystore",
    keystore_file,
    "-storepass",
    keystore_password,
    "-signedjar",
    signed_apk_file,
    apk_file,
    alias_name,
]
subprocess.run(jarsigner_command)

apksigner_command = [
    "java",
    "-jar",
    "C:\\Users\\ADMIN\\AppData\\Local\\Android\\Sdk\\build-tools\\34.0.0\\lib\\apksigner.jar",
    "sign",
    "--ks",
    keystore_file,
    "--ks-pass",
    "pass:" + keystore_password,
    "--out",
    signed_apk_file,
    apk_file,
]
subprocess.run(apksigner_command)
