import json
import munch

def json2obj(data):
    # print("============================")
    # print(type(data))
    # print("============================")
    if (type(data) is str):
        data = json.loads(data)
    data = munch.munchify(data)
    return data

def load(data):
    return json.loads(data)

def dump(data, file=None):
    if(file):
        return json.dump(data, file, indent=4, ensure_ascii=False)
    return json.dumps(data, indent=4, ensure_ascii=False)