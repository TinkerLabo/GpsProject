# from PIL import Image

# im = Image.open('./jpgs/KandaMyoujin_small.jpg')
# # im = Image.open('./jpgs/YushimaSeidouSeimon.jpg')

# exif = im._getexif()
# if exif:
#     for id, value in exif.items():
#         print(id, value)
# else:
#     print("Sorry, image has no exif data.")
from PIL import Image
import PIL.ExifTags as ExifTags
import reverse_geocoder as rg
from PIL.ExifTags import TAGS
import glob
import os
import sys
import csv
import traceback

def getExifMap(path):
    # 画像ファイルを開く --- (*1)
    im = Image.open(path)

    # print("#  ExifTags.TAGS:",ExifTags.TAGS)

    # exif = im._getexif()
    # if exif:
    #     for k, v in exif.items():
    #         print(k, v)
    # try:
    #     exif = im._getexif()
    #     exif_table = {}
    #     for tag_id, value in exif.items():
    #         tag = TAGS.get(tag_id, tag_id)
    #         print("# ",tag," val:",value)
    #         exif_table[tag] = value
    # except AttributeError:
    #     return {}

    exif = im._getexif()
    if exif == None:
        return None

    # EXIF情報を辞書型で得る(※注意、後置、内包表記)
    exif_table = {
        ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in ExifTags.TAGS
    }
    return exif_table

def get_gps(path):
    exif_table = getExifMap(path)
    if exif_table == None:
        return 0,0,0
    datetime = exif_table.get("DateTimeOriginal")
    print("# datetime_tags:",datetime)
    # GPS情報を得る --- (*2)
    if "GPSInfo" not in exif_table:
        print("no GPSInfo")
        return 0,0,datetime

    gps_tags = exif_table["GPSInfo"]
    gps = {
        ExifTags.GPSTAGS.get(t, t): gps_tags[t]
        for t in gps_tags
    }
    # 緯度経度情報を得る --- (*3)
    lat = conv_deg(gps["GPSLatitude"])
    lat_ref = gps["GPSLatitudeRef"]
    if lat_ref != "N": lat = 0 - lat
    lon = conv_deg(gps["GPSLongitude"])
    lon_ref = gps["GPSLongitudeRef"]
    if lon_ref != "E": lon = 0 - lon
    return lat, lon, datetime

def conv_deg(v):
    # 分数を度に変換
    d = float(v[0][0]) / float(v[0][1])
    m = float(v[1][0]) / float(v[1][1])
    s = float(v[2][0]) / float(v[2][1])
    return d + (m / 60.0) + (s / 3600.0)

# 撮影日付も拾う
# 緯度経度で地図にプロットする（LeafPad）
# 参考
# https://news.mynavi.jp/article/zeropython-42/
# pip install --upgrade reverse_geocoder
if __name__ == "__main__":
    with open('gpsinfo.tsv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        try:
            path ="./jpgs/*"
            for path in glob.glob(path):
                print(path)
                # lat, lon = get_gps('./jpgs/YushimaSeidouSeimon.jpg')
                lat, lon, datetime = get_gps(path)
                if lat!=0 and lon !=0:
                    # https://pypi.org/project/reverse_geocoder/
                    print(lat, lon)
                    # 都市名を調べる
                    results = rg.search([(lat, lon)])
                    print(results)
                    # 分かりやすく表示
                    area = {t: results[0][t] for t in results[0]}
                    print(area['cc'], area['admin1'], area['name'])
                    rec=[datetime, path, lat, lon, area['cc'], area['admin1'], area['name']]
                    writer.writerow(rec)
        except Exception as e:
            print("#ERROR:",os.path.abspath(path))
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))

