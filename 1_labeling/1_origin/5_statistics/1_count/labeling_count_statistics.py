import numpy as np
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

import cv2

# train하기 위해 만들어 놓은 원본 xml 전체 (data_process\xml)
xmlRootpath=r"D:\HN_code\test\1_labeling\15_10class_object_count_statistics\1_6class_data_process\class6_xml"

# 모든 class들을 0으로 초기화시키기
person_count=0
car_count=0
bus_count=0
truck_count=0
excavator_count=0
forklift_count=0
laddertruck_count=0
unknwncar_count=0
bicycle_count=0
motorbike_count=0

total_car=0
total_bus=0
total_truck=0
total_excavator=0
total_forklift=0
total_laddertruck=0
total_unknwncar=0
total_bicycle=0
total_motorbike=0
total_person=0

xmin_list=[]
xmax_list=[]
ymax_list=[]
ymin_list=[]
xlen_list=[]
ylen_list=[]
area_list=[]
name_list=[]
xml_list=[]

car_count_list=[]
bus_count_list=[]
truck_count_list=[]
excavator_count_list=[]
forklift_count_list=[]
laddertruck_count_list=[]
unknwncar_count_list=[]
bicycle_count_list=[]
motorbike_count_list=[]
person_count_list=[]

total_car_count_list=[]
total_bus_count_list=[]
total_truck_count_list=[]
total_excavator_count_list=[]
total_forklift_count_list=[]
total_laddertruck_count_list=[]
total_unknwncar_count_list=[]
total_bicycle_count_list=[]
total_motorbike_count_list=[]
total_person_count_list=[]

total_xml_list=[]

car_xlen=[]
car_ylen=[]
car_area=[]

person_xlen=[]
person_ylen=[]
person_area=[]

bus_xlen=[]
bus_ylen=[]
bus_area=[]

excavator_xlen=[]
excavator_ylen=[]
excavator_area=[]

truck_xlen=[]
truck_ylen=[]
truck_area=[]

forklift_xlen=[]
forklift_ylen=[]
forklift_area=[]

laddertruck_xlen=[]
laddertruck_ylen=[]
laddertruck_area=[]

unknwncar_xlen=[]
unknwncar_ylen=[]
unknwncar_area=[]

bicycle_xlen=[]
bicycle_ylen=[]
bicycle_area=[]

motorbike_xlen=[]
motorbike_ylen=[]
motorbike_area=[]

namelist=['person', 'car', 'bus', 'truck', 'excavator', 'forklift', 'ladder truck', 'unknown car' ,'bicycle', 'motorbike']

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
	    n = np.fromfile(filename, dtype)
	    img = cv2.imdecode(n, flags)

	    return img
    except Exception as e:
	    print(e)
	    return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


ONLY_MAKE_DOCUMENTS = False

for (path, dir, files) in os.walk(xmlRootpath):
    for cvatxml in files:
        if cvatxml.endswith(".xml"):

            tree = ET.parse(os.path.join(path,cvatxml))
            note = tree.getroot()
            for child in note.findall('object'):
                name = child.find('name').text
                # 기본적으로 한개도 안쳐져있는 경우 cvatxmls에 기록이 안됨.

                if name == "car":
                    name_list.append("person")
                    car_count+=1
                    total_car+=1
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    car_xlen.append(xlen)
                    car_ylen.append(ylen)
                    car_area.append(area)
                    #평균구하기
                    #print('car:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s ,xlen:%s,ylen:%s,area:%s'%(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:car   :xmin:%s    ymin:%s    xmax:%s    ymax:%s    xlen:%s    ylen:%s    area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                if name == "bus":
                    bus_count+=1
                    total_bus+=1
                    name_list.append("vehicle")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)
                    #print('bus:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s'%(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:bus   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    bus_xlen.append(xlen)
                    bus_ylen.append(ylen)
                    bus_area.append(area)

                if name == "person":
                    person_count +=1
                    total_person +=1
                    name_list.append("cycle")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    person_xlen.append(xlen)
                    person_ylen.append(ylen)
                    person_area.append(area)
                    #print('person:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s'%(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))


                if name == "truck":
                    truck_count +=1
                    total_truck +=1
                    name_list.append("motorbike")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen

                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)


                    truck_xlen.append(xlen)
                    truck_ylen.append(ylen)
                    truck_area.append(area)
                    #print('truck:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s'%(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:truck   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))

                if name == "excavator":
                    excavator_count +=1
                    total_excavator +=1
                    name_list.append("dog")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen

                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    excavator_xlen.append(xlen)
                    excavator_ylen.append(ylen)
                    excavator_area.append(area)
                    #print('excavator:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s' %(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:excavator   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                if name == "forklift":
                    forklift_count +=1
                    total_forklift +=1
                    name_list.append("traffic light")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    forklift_xlen.append(xlen)
                    forklift_ylen.append(ylen)
                    forklift_area.append(area)

                    #print('forklift:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s' %(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:forklift   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                if name == "laddertruck":
                    laddertruck_count +=1
                    total_laddertruck +=1
                    name_list.append("umbrella")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    laddertruck_xlen.append(xlen)
                    laddertruck_ylen.append(ylen)
                    laddertruck_area.append(area)

                    #print('ladder truck:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s' %(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:truck   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                if name == "unknown car":
                    unknwncar_count+=1
                    total_unknwncar+=1
                    name_list.append("face")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    unknwncar_xlen.append(xlen)
                    unknwncar_ylen.append(ylen)
                    unknwncar_area.append(area)

                    #print('unknown car:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s' %(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:unknown car   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                if name == "bicycle":
                    bicycle_count+=1
                    total_bicycle+=1
                    name_list.append("license plate")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    bicycle_xlen.append(xlen)
                    bicycle_ylen.append(ylen)
                    bicycle_area.append(area)

                    #print('bicycle:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s' %(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:bicycle   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                if name == "motorbike":
                    motorbike_count+=1
                    total_motorbike+=1
                    name_list.append("kick board")
                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    xlen = abs(xmin-xmax)
                    ylen = abs(ymin-ymax)
                    area=xlen*ylen
                    xmin_list.append(xmin)
                    ymin_list.append(ymin)
                    xmax_list.append(xmax)
                    ymax_list.append(ymax)
                    xlen_list.append(xlen)
                    ylen_list.append(ylen)
                    area_list.append(area)
                    xml_list.append(cvatxml)

                    motorbike_xlen.append(xlen)
                    motorbike_ylen.append(ylen)
                    motorbike_area.append(area)

                    #print('motorbike:xmin:%s ,ymin:%s ,xmax:%s, ymax:%s,xlen:%s,ylen:%s,area:%s' %(xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
                    #file2.write('name:%s   class:motorbike   :xmin:%s   ymin:%s   xmax:%s   ymax:%s   xlen:%s   ylen:%s   area:%s\n'%(cvatxml,xmin,ymin,xmax,ymax,xlen,ylen,xlen*ylen))
        car_count_list.append(car_count)
        bus_count_list.append(bus_count)
        person_count_list.append(person_count)
        truck_count_list.append(truck_count)
        excavator_count_list.append(excavator_count)
        forklift_count_list.append(forklift_count)
        laddertruck_count_list.append(laddertruck_count)
        unknwncar_count_list.append(unknwncar_count)
        bicycle_count_list.append(bicycle_count)
        motorbike_count_list.append(motorbike_count)
        #print('car:%s,bus:%s,person:%s,truck:%s,excavator:%s,forklift:%s,laddertruck:%s,unknowncar:%s,bicyle:%s,motorbike:%s'%(car_count,bus_count,person_count,
                                                                                                                        # truck_count,excavator_count,forklift_count,laddertruck_count,
                                                                                              #                                  unknwncar_count,bicycle_count,motorbike_count))


        car_count=0
        bus_count=0
        person_count=0
        truck_count=0
        excavator_count=0
        forklift_count=0
        laddertruck_count=0
        unknwncar_count=0
        bicycle_count=0
        motorbike_count=0
    #print(cvatxml)
print("--------------------")

total_car_count_list.append(total_car)
total_bus_count_list.append(total_bus)
total_person_count_list.append(total_person)
total_truck_count_list.append(total_truck)
total_excavator_count_list.append(total_excavator)
total_forklift_count_list.append(total_forklift)
total_laddertruck_count_list.append(total_laddertruck)
total_unknwncar_count_list.append(total_unknwncar)
total_bicycle_count_list.append(total_bicycle)
total_motorbike_count_list.append(total_motorbike)

print("total car:%s" %total_car)
print("total bus:%s" %total_bus)
print("total person:%s" %total_person)
print("totaltruck:%s" %total_truck)
print("total excavator:%s" %total_excavator)
print("total forklift:%s" %total_forklift)
print("total laddertruck:%s" %total_laddertruck)
print("total unknwncar:%s" %total_unknwncar)
print("total bicycle:%s" %total_bicycle)
print("total motorbike:%s" %total_motorbike)
