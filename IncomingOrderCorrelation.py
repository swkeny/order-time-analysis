from collections import OrderedDict
import xml.etree.ElementTree as ET
import os

# ideally all loader files would be in one folder, and all loader files in another folder
inboundOrderPath = 'C:/Users/deifen/PycharmProjects/OrderCorrelation/order-time-analysis/Data/IncomingOrders'
inboundOrdersSet = {}
inboundOrderFileCount = 0
inboundOrdersFiltered = 0
inboundOrdersTotal = 0
allocationCount = 0
fileCount = 0
PENDING_STATUS_FILTER = "PENDING"

print("Building Inbound Orders set...")

# loop through each file in the specified path
for filename in os.listdir(inboundOrderPath):
    fileCount += 1
    inboundOrderFileCount += 1
    tree = ET.parse(os.path.join(inboundOrderPath, filename))
    root = tree.getroot()
# strip time elements from filename, and convert to seconds elapsed since midnight
    timestamp = filename[-13:filename.find(".xml")]
    hours = timestamp[0:2]
    minutes = timestamp[2:4]
    seconds = timestamp[4:6]
    subseconds = timestamp[6:]
    timeInSeconds = float(str(int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)) + "." + subseconds)
# collect all the attributes common to the whole file
    for child in root:
        if child.tag == "portId":
            portId = child.text
        if child.tag == "typ":
            type = child.text
# find all Order elements in the xml file, and loop through to extract the attributes of each order
    orders = tree.findall(".//Order")
    for o in orders:
        order = OrderedDict()
        inboundOrdersTotal += 1
        for child in o:
            if child.tag == "allocId":
                allocId = child.text
            if child.tag == "status":
                status = child.text
# if the order status is PENDING, then build the order and add it to the order set
        if status == PENDING_STATUS_FILTER:
            allocationCount += 1
            order["allocId"] = allocId
            order["typ"] = type
            order["status"] = status
            order["portId"] = portId
            order["timeInSeconds"] = timeInSeconds
            inboundOrdersSet[allocId] = order
# keep track of how many orders were filtered with status <> PENDING
        else:
            inboundOrdersFiltered += 1

print("Inbound Orders set complete")
print("Saving to disk...")

columnHeaders = "AllocID, MessageType, Status, PortID, SecondsFromMidnight"
inboundOrders = [columnHeaders]

# loop through order set and prepare for output to file by packaging as a comma delimited string

for o in inboundOrdersSet.keys():
    tString = ""
    k = 1
    for i in inboundOrdersSet[o].keys():
# lets not add a comma after the last element in the set......
        if k == len(inboundOrdersSet[o]):
            tString += (str(inboundOrdersSet[o][i]))
        else:
            tString += (str(inboundOrdersSet[o][i])) + ", "
        k += 1
    inboundOrders.append(tString)

f2 = open('inboundOrders.txt', 'w')

for line in inboundOrders:
  f2.write("%s\n" % line)

f2.close()

# print run stats
print("Save complete")
print("Found " + str(allocationCount) + " allocations in " + str(fileCount) + " files")
print("Filtered " + str(inboundOrdersFiltered) + " orders out of a total of " + str(inboundOrdersTotal))