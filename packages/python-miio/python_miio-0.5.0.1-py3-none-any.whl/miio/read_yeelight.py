import html
import xml.etree.ElementTree as ET
import json

import logging
logging.basicConfig()
_LOGGER = logging.getLogger(__name__)

from extract_tokens import DeviceConfig

x = ET.parse("data/miot.xml")
devicelist = x.find("//set[@name='deviceList']")
if not devicelist:
    _LOGGER.warning("Unable to find deviceList")

for dev_elem in list(devicelist):
    dev = json.loads(dev_elem.text)
    ip = dev['localip']
    mac = dev['mac']
    model = dev['model']
    name = dev['name']
    token = dev['token']


    config = DeviceConfig(name=name, ip=ip, mac=mac, model=model,
                          token=token, everything=dev)
    print(config)