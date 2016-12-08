import xml.etree.ElementTree as ET
import os
import time

# ideally all cache server files would be in one folder, and all loader files in another folder
outboundOrderPath = 'C:/Users/deifen/PycharmProjects/OrderCorrelation/order-time-analysis/Data/OutgoingOrders'
inboundOrderPath = 'C:/Users/deifen/PycharmProjects/OrderCorrelation/order-time-analysis/Data/IncomingOrders'
outboundOrdersSet = {}
inboundOrdersSet = {}
PENDING_STATUS_FILTER = "PENDING"
outboundOrderFileCount = 0
inboundOrderFileCount = 0
inboundOrdersFiltered = 0
ordersMatched = 0

for filename in os.listdir(outboundOrderPath):
    outboundOrderFileCount += 1
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
        order["portId"] = portId
        order["typ"] = type

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
    inboundOrderFileCount += 1
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
        else:
            inboundOrdersFiltered += 1

for order in list(outboundOrdersSet.keys()):
    if order in inboundOrdersSet:
        # print(order)
        ordersMatched += 1
        
# Validate.....
print("Outbound files: " + str(outboundOrderFileCount))
print("Outbound orders: " + str(len(outboundOrdersSet)))
print("Incoming files: " + str(inboundOrderFileCount))
print("Incoming orders after filter: " + str(len(inboundOrdersSet)))
print("Incoming orders filtered: " + str(inboundOrdersFiltered))
print("Orders matched: " + str(ordersMatched))
# print(outboundOrdersSet["1"])
# print(generatedOrdersSet["CRD_49955655"])
# print(inboundOrdersSet["21"])
# print(ordersUpdateSet["CRD_49955587"])