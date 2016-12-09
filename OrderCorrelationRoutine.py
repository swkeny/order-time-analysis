import xml.etree.ElementTree as ET
import os
import csv

# ideally all cache server files would be in one folder, and all loader files in another folder
outboundOrderPath = ''
inboundOrderPath = ''

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
        timestamp = filename[-13:filename.find(".xml")]
        hours = timestamp[0:2]
        minutes = timestamp[2:4]
        seconds = timestamp[4:6]
        subseconds = timestamp[6:]
        timeInSeconds = float(str(int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)) + "." + subseconds)
        order["timeInSeconds"] = timeInSeconds
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
            timestamp = filename[-13:filename.find(".xml")]
            hours = timestamp[0:2]
            minutes = timestamp[2:4]
            seconds = timestamp[4:6]
            subseconds = timestamp[6:]
            timeInSeconds = float(str(int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)) + "." + subseconds)
            order["timeInSeconds"] = timeInSeconds
            # Add the order to the order set
            inboundOrdersSet[allocId] = order
        else:
            inboundOrdersFiltered += 1

for order in list(outboundOrdersSet.keys()):
    if order in inboundOrdersSet:
        print(inboundOrdersSet[order]["timeInSeconds"] - outboundOrdersSet[order]["timeInSeconds"])
        ordersMatched += 1

columnHeaders = "Order_Allocation_ID, Status, Message_Type, Seconds_Since_Midnight, Port_ID"
outboundOrders = [columnHeaders]
inboundOrders = [columnHeaders]


for o in outboundOrdersSet:
    tString = ""
    k = 1
    for i in outboundOrdersSet[o]:
        if k == len(outboundOrdersSet[o]):
            tString += (str(outboundOrdersSet[o][i]))
        else:
            tString += (str(outboundOrdersSet[o][i])) + ", "
        k += 1
    outboundOutputString = o + ", " + tString
    outboundOrders.append(outboundOutputString)

for o in inboundOrdersSet:
    tString = ""
    k = 1
    for i in inboundOrdersSet[o]:
        if k == len(inboundOrdersSet[o]):
            tString += (str(inboundOrdersSet[o][i]))
        else:
            tString += (str(inboundOrdersSet[o][i])) + ", "
        k += 1
    inboundOutputString = o + ", " + tString
    inboundOrders.append(inboundOutputString)

f1 = open('outboundOrders.txt', 'w')
f2 = open('inboundOrders.txt', 'w')

for line in outboundOrders:
  f1.write("%s\n" % line)

for line in inboundOrders:
  f2.write("%s\n" % line)


#
# wr = csv.writer(f, quoting=csv.QUOTE_NONE)
# wr.writerow(outboundOrders)








