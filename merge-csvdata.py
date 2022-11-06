import glob
import csv
import datetime

files = sorted(glob.glob("dat\\*"))
mergedata = []
dt_et = datetime.datetime(year=2022, month=10, day=27, hour=14, minute=37, second=50)


for i, file in enumerate(files):
    filename = file.split("\\")
    if i == 0:
        start = filename[1][8:23]
    dt_st = datetime.datetime.strptime(filename[1][8:23], "%Y%m%d %H%M%S")
    """
    if (dt_st - dt_et).seconds == 10:
        print(" continuity")
    else:
        print(" not continuity")
    """
    dt_et = datetime.datetime.strptime(filename[1][25:40], "%Y%m%d %H%M%S")

    with open(file) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        mergedata += data

end = filename[1][25:40]

Tsum = [1700.0]
length = len(mergedata)
cdata = reversed(mergedata)
for i, element in enumerate(cdata, 1):
    mean = sum(Tsum) / i
    if mean - 300 > float(element[1]):
        del mergedata[length - i]
        Tsum.append(mean)
    else:
        Tsum.append(float(element[1]))

with open(f"data____{start}--{end}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(mergedata)
