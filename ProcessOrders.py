# !/bin/python
from collections import OrderedDict
import xml.etree.ElementTree as ET
import os


def process_orders(path, direction = 'in'):

    recordset = {}

    for filename in os.listdir(path):
        dom = get_dom_tree(path, filename)
        orders = dom.findall(".//Order")
        timestamp = parse_time(filename)
        for order in orders:
            if direction == 'in':
                record = build_incoming_order_record(order, timestamp, dom)
            else:
                record = build_outgoing_order_record(order, timestamp, dom)
            if bool(record):
                recordset[record['allocId']] = record
    return recordset


def get_dom_tree(path, filename):
    return ET.parse(os.path.join(path, filename))


def parse_time(order):
    '''
    Takes an order file and parses out the creation time from the file name
    :param order: a filename that represents an order
    :return: time in seconds since midnight
    '''
    timestamp = order[-13:order.find(".xml")]
    hours = timestamp[0:2]
    minutes = timestamp[2:4]
    seconds = timestamp[4:6]
    subseconds = timestamp[6:]
    return float(str(int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)) + "." + subseconds)


def get_incoming_order_attributes(dom):
    '''

    :param dom:
    :return:
    '''
    root = dom.getroot()
    for child in root:
        if child.tag == "portId":
            portId = child.text
        if child.tag == "typ":
            type = child.text
    return portId, type


def get_outgoing_order_attributes(dom):
    '''

    :param dom:
    :return:
    '''
    root = dom.getroot()
    progId = None
    for child in root:
        if child.tag == "progId":
            progId = child.text
    return progId


def build_incoming_order_record(order, timestamp, dom):
    record = OrderedDict()

    portId, type = get_incoming_order_attributes(dom)

    for child in order:
        if child.tag == "allocId":
            allocId = child.text
        if child.tag == "status":
            status = child.text

    # if the order status is PENDING, then build the order and add it to the order set
    if status == "PENDING":

        record["allocId"] = allocId
        record["type"] = type
        record["status"] = status
        record["portId"] = portId
        record["timeInSeconds"] = timestamp

    return record


def build_outgoing_order_record(order, timestamp, dom):
    record = OrderedDict()

    progId = get_outgoing_order_attributes(dom)

    for child in order:
        if child.tag == "Allocation":
            # find the attributes of each allocation under the current order
            for a in child.getchildren():
                if a.tag == "allocId":
                    allocId = int(a.text)
                if a.tag == "portId":
                    portId = a.text
            # build the order, and add it to the order set
            record["allocId"] = allocId
            record["progId"] = progId
            record["portId"] = portId
            record["timeInSeconds"] = timestamp

    return record


def records_to_csv(recordset, columnHeaders, filename):

    orders = [columnHeaders]

    for o in recordset.keys():
        tString = ""
        k = 1
        for i in recordset[o].keys():
            # lets not add a comma after the last element in the set......
            if k == len(recordset[o]):
                tString += (str(recordset[o][i]))
            else:
                tString += (str(recordset[o][i])) + ", "
            k += 1
        orders.append(tString)

    f2 = open(filename, 'w')

    for line in orders:
        f2.write("%s\n" % line)

    f2.close()


results = process_orders('/Users/chip/Dropbox/code/order-time-analysis/data/IncomingOrders', 'in')
columnHeaders = "AllocID, MessageType, Status, PortID, SecondsFromMidnight"
records_to_csv(results, columnHeaders, 'inbound_orders.txt')

results = process_orders('/Users/chip/Dropbox/code/order-time-analysis/data/OutgoingOrders', 'out')
columnHeaders = "AllocID, ProgID, PortID, SecondsFromMidnight"
records_to_csv(results, columnHeaders, 'outbound_orders.txt')
