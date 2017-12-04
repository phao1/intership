from lxml import etree, objectify
tree = etree.parse("xmltest1.xml")
# get bbox
for bbox in tree.xpath("//ignored_region"):
    for corner in bbox.getchildren():
        print corner.text