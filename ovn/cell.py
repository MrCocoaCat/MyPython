import json


class cell():
    def _no__init(self, l):
        if isinstance(l, list) and len(l) == 2:
            self.type = l[0]
            self.val = l[1]
                                             





a = '{"data":[[["uuid","0aa86604-e1b7-4d49-aa57-f7ee669a1eff"],["set",[]],["set",[]],["map",[]],["set",[]],"ls1",["map",[]],["uuid","189736f3-459c-4594-80ba-cc76be115a00"],["set",[]]]],"headings":["_uuid","acls","dns_records","external_ids","load_balancer","name","other_config","ports","qos_rules"]}'

js = json.loads(a)
print js
data = js["data"]
head = js["headings"]


print data[0]
print head

