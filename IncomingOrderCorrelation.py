import xml.etree.ElementTree as ET
import os
import csv

# ideally all cache server files would be in one folder, and all loader files in another folder
inboundOrderPath = 'C:/Users/deifen/PycharmProjects/OrderCorrelation/order-time-analysis/Data/IncomingOrders'

inboundOrdersSet = {}
PENDING_STATUS_FILTER = "PENDING"
inboundOrderFileCount = 0
inboundOrdersFiltered = 0
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

columnHeaders = "COLUMN1, COLUMN2, COLUMN3, COLUMN4, COLUMN5"
inboundOrders = [columnHeaders]

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

f2 = open('inboundOrders.txt', 'w')

for line in inboundOrders:
  f2.write("%s\n" % line)

f2.close()