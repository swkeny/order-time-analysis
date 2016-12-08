import xml.etree.ElementTree as ET
import os
import time

# ideally all cache server files would be in one folder, and all loader files in another folder
# outboundOrderPath = ''
# inboundOrderPath = ''
outboundOrderPath = 'C:/Users/deifen/PycharmProjects/OrderCorrelation/order-time-analysis/Data/OutgoingOrders'
inboundOrderPath = 'C:/Users/deifen/PycharmProjects/OrderCorrelation/order-time-analysis/Data/IncomingOrders'
outboundOrdersSet = {}
inboundOrdersSet = {}

for filename in os.listdir(outboundOrderPath):
    PENDING_STATUS_FILTER = "PENDING"
    tree = ET.parse(os.path.join(outboundOrderPath, filename))
    root = tree.getroot()
    # print(filename)
    order = {}
    for child in root:
        # collect all the attributes common to the whole file. Still Need to exclude Order and add create time from filename.....
        if child.tag == "portId":
            portId = child.text
        if child.tag == "typ":
            type = child.text
        order["typ"] = type
        order["portId"] = portId

    orders = tree.findall(".//Order")
    for o in orders:
        for child in o:
            # Find the attributes of each order in the order list
            if child.tag == "allocId":
                allocId = child.text
            if child.tag == "status":
                status = child.text
        order["status"] = status
        order["timestamp"] = filename[-13:filename.find(".xml")]
        # Add the order to the order set
        outboundOrdersSet[allocId] = order

for filename in os.listdir(inboundOrderPath):
    tree = ET.parse(os.path.join(inboundOrderPath, filename))
    root = tree.getroot()
    # print(filename)
    order = {}
    for child in root:
        # collect all the attributes common to the whole file. Still Need to exclude Order and add create time from filename.....
        if child.tag == "portId":
            portId = child.text
        if child.tag == "typ":
            type = child.text
        order["typ"] = type
        order["portId"] = portId

    orders = tree.findall(".//Order")
    for o in orders:

        for child in o:
            # Find the attributes of each order in the order list
            if child.tag == "allocId":
                allocId = child.text
            if child.tag == "status":
                status = child.text
        if status == PENDING_STATUS_FILTER:
            order["status"] = status
            order["timestamp"] = filename[-13:filename.find(".xml")]
            # Add the order to the order set
            inboundOrdersSet[allocId] = order

for order in list(outboundOrdersSet.keys()):
    if order in inboundOrdersSet:
        print(order)

# Validate.....
print(outboundOrdersSet["1"])
# print(generatedOrdersSet["CRD_49955655"])
print(inboundOrdersSet["21"])
# print(ordersUpdateSet["CRD_49955587"])