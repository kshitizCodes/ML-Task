import json
import re
from createROIs import createROIs
import collections

regex = {
    "buyer": re.compile(r"Buyer.*\n([\s\S]+)"),
    "container": re.compile(r"[A-Z]{4}[0-9]{7}"),
    "eta": re.compile(r"ETA.*(\d{4}(?:\/\d{2}){2})"),
    "etd": re.compile(r"ETD.*(\d{4}(?:\/\d{2}){2})"),
    "hbl_num": re.compile(r"([A-Z0-9]{9}) *[A-Z0-9]{9}"),
    "hbl_scac": re.compile(r"SCAC.*\n([A-Z]{4}) [A-Z]{4}"),
    "mbl_num": re.compile(r"[A-Z0-9]{9} *([A-Z0-9]{9})"),
    "mbl_scac": re.compile(r"SCAC.*\n[A-Z]{4} ([A-Z]{4})"),
    "seller": re.compile(r"Seller.*\n([\s\S]+)"),
    "pod": re.compile(r"POD *\n([A-Za-z, ]+)"),
    "pol": re.compile(r"POL *\n([A-Za-z, ]+)"),
    "type_of_movement": re.compile(r"(FCL *[A-Za-z]+|LCL *[A-Za-z]+)"),
    "vessel_name": re.compile(r"Vessel *\/ *Voyage *\n([A-Z ]+)"),
    "voyage_num": re.compile(r"\b([A-Z0-9]{5})\b *\n*ETA of POD"),
}

texts = createROIs()
output = {}

for text in texts:
    for key in regex:
        match = re.findall(regex[key], text)
        if len(match) > 0:
            output[key] = str(match.pop()).replace("\n", " ")
            output[key] = re.sub("[^A-Za-z0-9.,\n ]", "", output[key])
            if re.search(r"LCL.*", output[key]):
                output[key] = re.sub("LCL.*", "LCL", output[key])
            elif re.search(r"FCL.*", output[key]):
                output[key] = re.sub("FCL.*", "FCL", output[key])

with open("extraction.json", "w") as f:
    json = json.dumps([output], indent=4, sort_keys=True)
    f.write(json)
    print(json)
