import cv2
import csv
import glob
import time
import datetime
import numpy as np


# accurate crop point set XY(UpperLeft, UpperRight, LowerRight, LowerLeft)
cropPoint = [[35, 20], [465, 33], [446, 150], [6, 142]]
# point for segment border YX
segborder = [
    [[10, 20], [36, 20], [70, 20], [100, 20]],
    [[10, 65], [36, 65], [70, 65], [100, 65]],
    [[10, 100], [36, 100], [70, 100], [100, 100]],
    [[10, 135], [36, 135], [70, 135], [100, 135]],
    [[10, 171], [36, 171], [70, 171], [100, 171]],
    [[10, 207], [36, 207], [70, 207], [100, 207]],
    [[10, 242], [36, 242], [70, 242], [100, 242]],
    [[10, 279], [36, 279], [70, 279], [100, 279]],
    [[10, 316], [36, 316], [70, 316], [100, 316]],
    [[10, 353], [36, 353], [70, 353], [100, 353]],
    [[10, 391], [36, 391], [70, 391], [100, 391]],
    [[10, 420], [36, 420], [70, 420], [100, 420]],
]
# segment 0-9 TF
segconf = [
    [True, True, True, True, True, True, False],  # 0
    [False, True, True, False, False, False, False],  # 1
    [True, True, False, True, True, False, True],  # 2
    [True, True, True, True, False, False, True],  # 3
    [False, True, True, False, False, True, True],  # 4
    [True, False, True, True, False, True, True],  # 5
    [True, False, True, True, True, True, True],  # 6
    [True, True, True, False, False, False, False],  # 7
    [True, True, True, True, True, True, True],  # 8
    [True, True, True, True, False, True, True],  # 9
]


def CropPic(src, pnts, dstsize):
    height, width = dstsize
    pts1 = np.float32(pnts)
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(src, M, (width, height))
    return dst


def withline(img, start, end):
    y, x = start
    starty, startx = segborder[y][x]
    y, x = end
    endy, endx = segborder[y][x]
    step = max(abs(starty - endy), abs(startx - endx))
    xstep = (endx - startx) / step
    ystep = (endy - starty) / step
    for i in range(step):
        if img[int(starty + ystep * i), int(startx + xstep * i)][0] > 0:
            return True
    return False


def segCheck(seg):
    i = 0
    for num in segconf:
        if seg == num:
            return i
        i += 1
    return 0


data = []
files = glob.glob("pic\\*")
step = 0
checklen = 46220  # --------------------------------------------------------
t = [time.time()] * 30
k = 1


for file in files[: checklen + 1]:
    # road
    img = cv2.imread(file)
    # roughly crop
    img = img[260:420, 0:480]

    cimg = CropPic(img, cropPoint, (110, 430))

    gray = cimg
    for i in range(110):
        for j in range(430):
            gray[i, j] = np.mean(cimg[i, j, :2])

    grmax = np.max(gray)
    thr = 245 if grmax >= 255 else 150 if grmax >= 220 else max(grmax - 120, 120)
    # print('\r',k, grmax, '\t', thr, end='')

    dst = gray
    for i in range(110):
        for j in range(430):
            dst[i, j] = 255 if gray[i, j, 0] > thr else 0

    file = file.split("\\")
    file[0] = "shp"
    dt_date = datetime.datetime.strptime(file[1][3:18], "%Y%m%d-%H%M%S")
    file = "\\".join(file)
    cv2.imwrite(file, dst)

    seg = [[False] * 7 for i in range(6)]
    for i in range(0, 11, 2):
        if i != 0:
            seg[int(i / 2)][0] = withline(dst, (i, 1), (i, 0))
            seg[int(i / 2)][1] = withline(dst, (i, 1), (i + 1, 1))
            seg[int(i / 2)][2] = withline(dst, (i, 2), (i + 1, 2))
            seg[int(i / 2)][3] = withline(dst, (i, 2), (i, 3))
            seg[int(i / 2)][4] = withline(dst, (i, 2), (i - 1, 2))
            seg[int(i / 2)][5] = withline(dst, (i, 1), (i - 1, 1))
            seg[int(i / 2)][6] = withline(dst, (i, 1), (i, 2))
        else:
            seg[int(i / 2)][1] = withline(dst, (i, 1), (i + 1, 1))
            seg[int(i / 2)][2] = withline(dst, (i, 2), (i + 1, 2))
    nums = ""
    for cell in seg:
        nums += str(segCheck(cell))

    gram = float(nums) / 100.0
    tmp = [dt_date.timestamp(), gram]
    data.append(tmp)

    t[step] = time.time()
    tps = (sum(t) - min(t) * len(t)) / len(t)
    td = datetime.timedelta(seconds=(checklen - i) * (tps if tps > 0 else 0))
    printstr = " {:6.2f}% ({:6d}/{:6d})  TREM:{:10} \t{:s}    ".format(
        k / checklen * 100.0,
        k,
        checklen,
        str(td - datetime.timedelta(microseconds=td.microseconds)),
        file,
    )
    print("\r" + " " * len(printstr) + "\r" + printstr, end="")
    step = (step + 1) % len(t)

    if k % 1000 == 1:
        dt_start = dt_date
    if k % 1000 == 0:
        starttime = dt_start.strftime("%Y%m%d %H%M%S")
        endtime = dt_date.strftime("%Y%m%d %H%M%S")
        with open(f"dat\\data____{starttime}--{endtime}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        data.clear()

    k += 1


starttime = dt_start.strftime("%Y%m%d %H%M%S")
endtime = dt_date.strftime("%Y%m%d %H%M%S")
with open(f"dat\\data____{starttime}--{endtime}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
