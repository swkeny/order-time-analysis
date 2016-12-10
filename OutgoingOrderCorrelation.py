from collections import OrderedDict
import xml.etree.ElementTree as ET
import os

# ideally all cache server files would be in one folder, and all loader files in another folder
outboundOrderPath = 'C:/Users/deifen/PycharmProjects/OrderCorrelation/order-time-analysis/Data/OutgoingOrders'
outboundOrdersSet = {}
outboundOrderFileCount = 0
allocationCount = 0
fileCount = 0

print("Building Outbound Orders set...")

# loop through each file in the specified path
for filename in os.listdir(outboundOrderPath):
    fileCount += 1
    outboundOrderFileCount += 1
    tree = ET.parse(os.path.join(outboundOrderPath, filename))
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
        if child.tag == "progId":
            progId = child.text
# find all Order elements in the xml file, and loop through them looking for Allocation elements
    orders = tree.findall(".//Order")
    for o in orders:
        for child in o:
            if child.tag == "Allocation":
                order = OrderedDict()
                allocationCount += 1
# find the attributes of each allocation under the current order
                for a in child.getchildren():
                    if a.tag == "allocId":
                        allocId = a.text
                    if a.tag == "portId":
                        portId = a.text
# build the order, and add it to the order set
                order["allocId"] = allocId
                order["progId"] = progId
                order["portId"] = portId
                order["timeInSeconds"] = timeInSeconds
                outboundOrdersSet[allocId] = order

print("Outbound Orders set complete")
print("Saving to disk...")

columnHeaders = "AllocID, ProgID, PortID, SecondsFromMidnight"
outboundOrders = [columnHeaders]

# loop through order set and prepare for output to file by packaging as a comma delimited string
for o in outboundOrdersSet:
    tString = ""
    k = 1
    for i in outboundOrdersSet[o]:
# lets not add a comma after the last element in the set......
        if k == len(outboundOrdersSet[o]):
            tString += (str(outboundOrdersSet[o][i]))
        else:
            tString += (str(outboundOrdersSet[o][i])) + ", "
        k += 1
    outboundOrders.append(tString)

f1 = open('outboundOrders.txt', 'w')

for line in outboundOrders:
  f1.write("%s\n" % line)

f1.close()

# print run stats
print("Save complete")
print("Found " + str(allocationCount) + " allocations in " + str(fileCount) + " files")





