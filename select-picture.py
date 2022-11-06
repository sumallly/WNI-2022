import os
import cv2
import tqdm
import glob

files = glob.glob("pic\\*")
count = 0

print("\nNow checking broken file. Wait a minute.")

for file in tqdm.tqdm(files):
    img = cv2.imread(file)

    # print('\r', file, end='')
    if img is None:
        # print('\nDETECTED!!!')
        count += 1
        os.remove(file)

print(f"\n{count} files are removed.")

files = sorted(glob.glob("pic\\*"))
i = 0
count = 0
while True:
    print("\r", i, end="")
    file = files[i]
    img = cv2.imread(file)
    cv2.putText(img, file, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    try:
        cv2.imshow("img", img)
    except Exception:
        print(file)
        break

    key = cv2.waitKey(1000)

    if key == 112:  # p
        # print('\r next 1000', end='')
        i += 1000

    elif key == 111:  # o
        # print('\r next 1', end='')
        i += 1

    elif key == 105:  # i
        # print('\r previous 1', end='')
        i -= 1

    elif key == 117:  # u
        # print('\r previous 1000', end='')
        i -= 1000

    elif key == 13:  # enter
        break

    else:
        i += 1

    if i < 0:
        i = 0
    elif i >= len(files):
        i = len(files) - 1

print("\n", i, file)
cv2.destroyAllWindows()
