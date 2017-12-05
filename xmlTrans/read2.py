from lxml import etree, objectify
from lxml import etree

def read(fileName):
    tree = etree.parse(fileName)
    list_data = []
    list_cycle =[]
    skip = 1
    for frameNumber in tree.xpath('//frame'):
        for item in frameNumber.attrib:
            if(skip%2):
                #print skip
                list_cycle.append(frameNumber.attrib[item])
                # print '@' + item + '=' + frameNumber.attrib[item]
            skip = skip +1
    #print list_cycle

    for df in tree.xpath('//frame//box'):
        # Iterate over attributes of datafield
        for attrib_name in df.attrib:
            list_data.append(df.attrib[attrib_name])
            boxes = df.getchildren()
        for box in boxes:
            list_data.append(box.text)
    #print list_data
    return (list_data,list_cycle)


def add(width, height, depth,list_data,list_cycle,file_sequence,data_sequence):
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
        addObject(left, top, (left + width), (top + height), E, anno_tree)
        cycle2 = cycle2 - 1

    file_sequence_fill =str(file_sequence+1).zfill(5)
    filename= "D:\software\work\dataset\output\MVI_20011\img" + file_sequence_fill +".xml"
    file_sequence=file_sequence+1
    #print "img",file_sequence
    etree.ElementTree(anno_tree).write(filename, pretty_print=True)
    return data_sequence


def addObject(xmin,ymin,xmax,ymax, E,anno_tree):
    E2 = objectify.ElementMaker(annotate=False)
    anno_tree2 = E2.object(
        E.name("car"),
        E.bndbox(
            E.xmin(xmin),
            E.ymin(ymin),
            E.xmax(xmax),
            E.ymax(ymax)
        ),
        E.difficult(0)
    )
    anno_tree.append(anno_tree2)

def main(fileName):
    list_data, list_cycle=read(fileName)
    file_sequence=0
    j=0
    data_sequence = 0
    for picture in list_cycle:
        data_sequence=add(960, 540, 3, list_data, list_cycle,file_sequence,data_sequence)
        file_sequence=file_sequence+1



fileName = "D:\software\work\dataset\DETRAC-Train-Annotations-XML\DETRAC-Train-Annotations-XML\MVI_20011.xml"
#D:\software\work\dataset\DETRAC-Train-Annotations-XML\DETRAC-Train-Annotations-XML\MVI_20011.xml
main(fileName)