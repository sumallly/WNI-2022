import cv2
import time
import datetime

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

capture_cycle = 10  # seconds

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({"q": "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    if file1["title"] == "picture":
        folder_pic = file1
        break

cap = cv2.VideoCapture(0)
print("start")

"""
filename = 'asample001.jpg'
IMG_P = filename
reader = easyocr.Reader(['en'])
RST = reader.readtext(IMG_P)
print(RST)
"""

while True:
    try:
        dt_now = datetime.datetime.now()
        sec = (int)(dt_now.strftime("%S"))
        print(sec)

        ret, frame = cap.read()
        if not ret:
            print("not capture")
            break

        key = cv2.waitKey(1)
        if key == 13:  # enter
            break

        if sec % capture_cycle == 0:
            filename = dt_now.strftime("pic/cap%Y%m%d-%H%M%S.jpg")
            cv2.imwrite(filename, frame)

            metadata = {
                "parents": [{"id": folder_pic["id"]}],
                "title": filename,
                "mimeType": "image/jpeg",
            }
            file0 = drive.CreateFile(metadata=metadata)
            file0.SetContentFile(filename)
            file0.Upload()
        time.sleep(1)

    except Exception as e:
        errorfile = dt_now.strftime("log/%Y%m%d-%H%M%S.txt")
        f = open(errorfile, "w")
        print(e)
        f.write(str(e))
        f.close
        time.sleep(20)

cv2.destroyAllWindows()
cap.release()
