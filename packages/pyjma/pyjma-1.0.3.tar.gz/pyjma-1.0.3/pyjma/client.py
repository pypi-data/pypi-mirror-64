import requests
from pyjma import earthquake
from pyjma import volcano
import re
from datetime import datetime as dt
from pyjma import util

def disaster_data(data_types = []):

    data = {"status": "OK", "results": []}

    if "earthquake" in data_types or "volcano" in data_types:

        namespaces = {"": 'http://www.w3.org/2005/Atom'}
        url = "http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml"

        root = util.get_xml(url)

        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
            if "earthquake" in data_types and title == "震源・震度に関する情報":
                item = earthquake.process_earthquake_data(entry)
                data["results"].append(item)
    return data
