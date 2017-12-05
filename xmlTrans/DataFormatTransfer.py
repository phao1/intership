from lxml import etree, objectify
from lxml import etree
def read(fileName):
    tree = etree.parse(fileName)
    list_data = []
    list_cycle =[]
    list_attribute = []
    carType = []
    fileSequence = []
    fileSequence2 = []
    skip = 1
    skip2 =4
    skip3 =1
    for frameNumber in tree.xpath('//frame'):
        for item in frameNumber.attrib:
            if(skip%2):
                #print skip
                list_cycle.append(frameNumber.attrib[item])
                # print '@' + item + '=' + frameNumber.attrib[item]
            skip = skip +1
    #print list_cycle

    for df in tree.xpath('//frame'):
        # Iterate over attributes of datafield
        for attrib_name in df.attrib:
            fileSequence.append(df.attrib[attrib_name])
            boxes = df.getchildren()
        for box in boxes:
            fileSequence.append(box.text)
    while (skip3<len(fileSequence)):
        fileSequence2.append(fileSequence[skip3])
        skip3= skip3+3


    for df in tree.xpath('//frame//box'):
        # Iterate over attributes of datafield
        for attrib_name in df.attrib:
            list_data.append(df.attrib[attrib_name])
            boxes = df.getchildren()
        for box in boxes:
            list_data.append(box.text)
            #print list_data

    for df in tree.xpath('//frame//attribute'):
        # Iterate over attributes of datafield
        for attrib_name in df.attrib:
            list_attribute.append(df.attrib[attrib_name])
            boxes = df.getchildren()
        for box in boxes:
            list_attribute.append(box.text)
    while (skip2<len(list_attribute)):
        carType.append(list_attribute[skip2])
        skip2= skip2+5

        #print carType
        #print "len(carType)",len(carType)
        #print "len(list_data)", len(list_data)
        #print carType
        #print list_attribute
    return (list_data,list_cycle,carType,fileSequence2)

def add(width, height, depth,list_data,list_cycle,file_sequence,data_sequence,carType,carNumber,fileSequence2):
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('test_folder'),
        E.filename("test.jpg"),
        E.source(
            E.database('COCO'),
            E.annotation('COCO'),
            E.image('COCO'),
            E.url("http://test.jpg")
        ),
        E.size(
            E.width(width),
            E.height(height),
            E.depth(depth)
        ),
        E.segmented(0),
    )
    cycle2 = int(list_cycle[file_sequence])

    while cycle2 > 0:
        width = int(round(float(list_data[(data_sequence + 2)])))
        height = int(round(float(list_data[data_sequence + 3])))
        top = int(round(float(list_data[data_sequence + 1])))
        left = int(round(float(list_data[data_sequence])))
        data_sequence = data_sequence + 4
        #print "i",data_sequence

        addObject(left, top, (left + width), (top + height), E, anno_tree,carType,carNumber)
        carNumber =  carNumber+1
        #print carNumber
        cycle2 = cycle2 - 1

    file_sequence_fill =str(int(fileSequence2[file_sequence])).zfill(5)
    filename= "D:\software\work\dataset\output\MVI_63552\img" + file_sequence_fill +".xml"
    #filename= "img" + file_sequence_fill +".xml"
    #filename= "D:\software\work\dataset\output\MVI_test\img" + file_sequence_fill +".xml"

    #fileSequence2[file_sequence]=fileSequence2[file_sequence]+1
    #print "img",file_sequence
    etree.ElementTree(anno_tree).write(filename, pretty_print=True)
    return data_sequence,carNumber


def addObject(xmin,ymin,xmax,ymax, E,anno_tree,carType,carNumber):
    E2 = objectify.ElementMaker(annotate=False)
    anno_tree2 = E2.object(
        E.name(carType[carNumber]),
        E.bndbox(
            E.xmin(xmin),
            E.ymin(ymin),
            E.xmax(xmax),
            E.ymax(ymax)
        ),
        E.difficult(0)
    )
    #print carType[carNumber]
    anno_tree.append(anno_tree2)

def main(fileName):
    list_data, list_cycle,carType,fileSequence2=read(fileName)
    carNumber = 0
    #print "len(carType)",len(carType)
    file_sequence=0
    j=0
    data_sequence = 0
    for picture in list_cycle:
        data_sequence,carNumber=add(960, 540, 3, list_data, list_cycle,file_sequence,data_sequence,carType,carNumber,fileSequence2)
        file_sequence=file_sequence+1



fileName = "D:\software\work\dataset\DETRAC-Train-Annotations-XML\DETRAC-Train-Annotations-XML\MVI_63552.xml"
#fileName ="test_sequnce.xml"
#D:\software\work\dataset\DETRAC-Train-Annotations-XML\DETRAC-Train-Annotations-XML\MVI_20011.xml
main(fileName)