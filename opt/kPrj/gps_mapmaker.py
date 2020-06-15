import folium

gps_list = []
gps_data = []
info=[]
with open('gpsinfo.tsv',mode='r',encoding='utf-8') as f:
    # next(f)
    for line in f:
        gps_list = line.rstrip('\n').split('\t')
        # print(gps_list[:2])
        # print(gps_list[2:4])
        info.append(gps_list[:2])
        gps_data.append(gps_list[2:4])

gps_data_flt = []
for d in gps_data:
    gps_data_flt.append([float(i) for i in d])
print(gps_data_flt)

last_log = gps_data_flt[-1]

# icon = folium.features.CustomIcon('http://www.pngall.com/wp-content/uploads/2016/05/Iron-Man.png', icon_size=(50,50))

# map = folium.Map(location=last_log,zoom_start=80)
# map = folium.Map(location=last_log,tiles="Stamen Toner",zoom_start=80)
map = folium.Map(location=last_log,tiles='Stamen Terrain',zoom_start=80)

for f,t in zip(gps_data_flt,info):
    icon = folium.features.CustomIcon(t[1], icon_size=(50,50))
    marker = folium.Marker(f,popup=t[1],icon=icon)
    # marker = folium.Marker(f,popup=t[1])
    map.add_child(marker)

gps_line = folium.PolyLine(locations=gps_data_flt)
map.add_child(gps_line)

map.save(outfile="gps_map.html")



