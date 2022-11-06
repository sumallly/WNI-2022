import os
import time
import pathlib
import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

print("\n Program start.")

gauth = GoogleAuth("setting.yaml")
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

print(" Auth OK.")

file_list = drive.ListFile({"q": "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    if file1["title"] == "picture":
        folder_pic = file1
        break

print(" Listing pictures.")

file_list2 = drive.ListFile(
    {"q": f"'{folder_pic['id']}' in parents", "orderBy": "title"}
).GetList()
checklen = len(file_list2)

i = 1
j = 0
t = [time.time()] * 30
status = "idle"
print(" Download start.")

for file2 in file_list2:

    picpath = file2["title"]
    downloadFile = drive.CreateFile({"id": file2["id"]})

    while True:
        try:
            if status == "exception":
                print()
            if os.path.isfile(picpath):
                # already downloaded
                status = "trash"
                if not file2["labels"]["trashed"]:
                    downloadFile.Trash()
                break

            else:
                status = "download"
                downloadFile.GetContentFile(picpath)
                break

        except Exception as e:
            dt_now = datetime.datetime.now()
            status = status[0] + "-" + "exception"
            errorfile = dt_now.strftime(
                f"log/{pathlib.Path(__file__).stem}-%Y%m%d-%H%M%S.txt"
            )
            f = open(errorfile, "w")
            print("\n", e)
            f.write(str(errorfile) + "\n" + str(picpath) + "\n" * 2 + str(e))
            f.close
            time.sleep(10)

        finally:
            t[j] = time.time()
            tps = (sum(t) - min(t) * len(t)) / len(t)
            td = datetime.timedelta(seconds=(checklen - i) * (tps if tps > 0 else 0))
            printstr = (
                "status:{:12s} {:6.2f}% ({:6d}/{:6d})  TREM:{:10} \t{:s}    ".format(
                    status,
                    i / checklen * 100.0,
                    i,
                    checklen,
                    str(td - datetime.timedelta(microseconds=td.microseconds)),
                    picpath,
                )
            )
            print("\r" + " " * len(printstr) + "\r" + printstr, end="")
            j = (j + 1) % len(t)
            if status != "exception":
                i += 1
                break

print("")
