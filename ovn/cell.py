import json


def recell(l):
    if isinstance(l, list) and len(l) == 2:
        if l[0] == "map":
            return dict(l[1])
        if l[0] == "set":
            return [recell(i) for i in l[1]]
        if l[0] == "uuid":
            return str(l[1])
    else:
        return l


a = '{"data":[[["uuid","0aa86604-e1b7-4d49-aa57-f7ee669a1eff"],["set",[]],["set",[]],["map",[]],["set",[]],"ls1",["map",[]],["set",[["uuid","189736f3-459c-4594-80ba-cc76be115a00"],["uuid","41948249-f750-4a0d-9b56-f5719a494f65"]]],["set",[]]]],' \
    '"headings":["_uuid","acls","dns_records","external_ids","load_balancer","name","other_config","ports","qos_rules"]}'

js = json.loads(a)
#print js
data = js["data"]
head = js["headings"]

data = [recell(i) for i in data[0]]

re = dict(zip(head, data))
#print re

for k, v in re.items():
    print k, v

#la = lambda x, y, z: x + y + z
#print(la(1, 2, 3))