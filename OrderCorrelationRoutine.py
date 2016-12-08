import xml.etree.ElementTree as ET
import os
import time

# ideally all cache server files would be in one folder, and all loader files in another folder
outboundOrderPath = '{path1}'
inboundOrderPath = '{path2}'
generatedOrdersSet = {}
ordersUpdateSet = {}

for filename in os.listdir(outboundOrderPath):
    tree = ET.parse(os.path.join(outboundOrderPath, filename))
    root = tree.getroot()
    # print(filename)
    order = {}
    for child in root:
        # collect all the attributes common to the whole file. Still Need to exclude Order and add create time from filename.....
        order[child.tag] = child.text

    orders = tree.findall(".//Order")
    for o in orders:
        for child in o:
            # Find the attributes of each order in the order list
            if child.tag == "allocId":
                allocId = child.text
            if child.tag == "status":
                status = child.text
        order['status'] = status
        order['timestamp'] = filename[-13:filename.find(".xml")]
        # Add the order to the order set
        generatedOrdersSet[allocId] = order

for filename in os.listdir(inboundOrderPath):
    tree = ET.parse(os.path.join(inboundOrderPath, filename))
    root = tree.getroot()
    # print(filename)
    order = {}
    for child in root:
        # collect all the attributes common to the whole file. Still Need to exclude Order and add create time from filename.....
        order[child.tag] = child.text

    orders = tree.findall(".//Order")
    for o in orders:

        for child in o:
            # Find the attributes of each order in the order list
            if child.tag == "allocId":
                allocId = child.text
            if child.tag == "status":
                status = child.text
        order['status'] = status
        order['timestamp'] = filename[-13:filename.find(".xml")]
        # Add the order to the order set
        ordersUpdateSet[allocId] = order

for order in list(generatedOrdersSet.keys()):
    if order in ordersUpdateSet:
        print(order)

# Validate.....
print(generatedOrdersSet["1"])
# print(generatedOrdersSet["CRD_49955655"])
print(ordersUpdateSet["21"])
# print(ordersUpdateSet["CRD_49955587"])