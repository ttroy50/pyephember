"""
Example script to watch MQTT messages
"""

import json
import base64
import argparse
import getpass
import datetime

from pyephember.pyephember import EphEmber


def ts_print(*stuff):
    """
    print with timestamp
    """
    return print(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"), *stuff)


def process_point_data(pstr):
    """
    Parse base64-encoded pointData into a dictionary
    Keys are the indices
    Values are (datatype, integer_value)
    where datatype is 1, 2, 4, 5 (see API.md)
    """
    lengths = {1: 1, 2: 2, 4: 2, 5: 4}
    parsed = {}
    mode = "wait"
    datatype = None
    index = None
    value = []

    def bytes_to_int(byte_data):
        """
        Convert bytes to an integer, naively
        """
        result = 0
        for a_byte in byte_data:
            result = result * 256 + int(a_byte)
        return result

    for number in base64.b64decode(pstr):
        if mode == "wait":
            assert number == 0
            mode = "index"
            continue
        if mode == "index":
            index = number
            mode = "datatype"
            continue
        if mode == "datatype":
            datatype = number
            if datatype not in lengths:
                raise RuntimeError("Unknown datatype: {}".format(datatype))
            mode = "value"
            continue
        if mode == "value":
            value.append(number)
            if len(value) == lengths[datatype]:
                parsed[index] = (datatype, bytes_to_int(value))
                value = []
                mode = "wait"
            continue
    return parsed


# pylint: disable=unused-argument

def on_log(client, userdata, level, buf):
    """
    Simple callback for logging
    """
    if args.show_log:
        ts_print("log: ({})".format(",".join(
            [str(x) for x in (userdata, level, buf)]
        )))


def on_connect(client, userdata, flags, result_code):
    """
    Simple callback on MQTT connection
    """
    ts_print("Connected with result code:", result_code)
    client.subscribe(POINTDATA_TOPIC_UPLOAD, 0)


def on_subscribe(client, userdata, mid, granted_qos):
    """
    Simple callback on MQTT subscription
    """
    ts_print("Subscribed with data: ({})".format(",".join(
        [str(x) for x in [userdata, mid, granted_qos]]
    )))


def on_message(client, userdata, message):
    """
    Decode and print message pointData
    """
    msg = str(message.payload.decode("utf-8").rstrip('\0'))
    if args.show_raw_messages:
        ts_print("raw message:", msg)
    j = json.loads(msg)
    if 'data' in j and 'pointData' in j['data']:
        ts_print('Decoded message pointData:',
                 process_point_data(j['data']['pointData']))


parser = argparse.ArgumentParser(
    prog='ember-watch',
    description='Watch EPH Ember MQTT "upload/pointdata" messages'
)
parser.add_argument(
    "--email", type=str, required=True, help="Email Address for your account"
)
parser.add_argument(
    '--password', type=str, default="", help="Password for your account"
)
parser.add_argument(
    '--show-log', action='store_true', help="Show MQTT client log"
)
parser.add_argument(
    '--show-raw-messages', action='store_true', help="Show undecoded messages"
)
args = parser.parse_args()

##################################################
# start

password = args.password
if not password:
    password = getpass.getpass()

t = EphEmber(args.email, password)
POINTDATA_TOPIC_UPLOAD = "/".join([
    t.get_home_details()['homes']['productId'],
    t.get_home_details()['homes']['uid'],
    "upload/pointdata"
])


st = t.messenger.start(
    on_connect=on_connect,
    on_log=on_log, on_message=on_message, on_subscribe=on_subscribe
)

while True:
    t.messenger.client.loop()
