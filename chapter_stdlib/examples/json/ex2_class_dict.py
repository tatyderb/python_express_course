# https://blog.softhints.com/python-convert-object-to-json-3-examples/
import json

class error:
    def __init__(self):
        self.errorCode="server issue"
        self.errorMessage="201"


class BaseRespone():
    def __init__(self):
        self.success = "data fetch successfully"
        self.data={"succss":"msg"}
        self.error1 = error()

def obj_to_dict(obj):
   return obj.__dict__


bs = BaseRespone()
# json_string = json.dumps(bs.__dict__,  default = obj_to_dict)
# json_string = json.dumps(bs,  default = obj_to_dict)
json_string = json.dumps(bs,  default = vars)
print('json_string=', json_string, type(json_string))

json_string1 = json.loads(json_string)
print('json_string1=', json_string1, type(json_string1))