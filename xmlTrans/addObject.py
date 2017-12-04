import urllib, urllib2
from lxml import etree, objectify
from lxml import etree
def add(width, height, depth,xmin,ymin,xmax,ymax):
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('VOC2014_instance'),
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
    addObject(24, 25, 26, 27,E, anno_tree)
    addObject(14, 15, 16, 17, E, anno_tree)
    etree.ElementTree(anno_tree).write("test5.xml", pretty_print=True)

def addObject(xmin,ymin,xmax,ymax, E,anno_tree):
    E2 = objectify.ElementMaker(annotate=False)
    anno_tree2 = E2.object(
        E.name("person"),
        E.bndbox(
            E.xmin(xmin),
            E.ymin(ymin),
            E.xmax(xmax),
            E.ymax(ymax)
        ),
        E.difficult(0)
    )
    anno_tree.append(anno_tree2)

add(1, 2, 3,4,5,6,7)