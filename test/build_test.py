dict1 = {'key': 'MYSQL_HOST', 'value': 'mysql_host1'}

dict2 = {'key': 'MYSQL_HOST', 'value': 'mysql_host'}

s1 = set(dict1.items())
s2 = set(dict2.items())

s3 = s1 ^ s2
print(s3)  # 差集
s3 = set(item[0] for item in s3)

print(list(s3))

import json

temp = []

result = json.dumps(temp)
print(result)
