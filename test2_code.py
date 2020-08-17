import re

file = open('test2.txt')

string = ''
for i in file:
	string += i

raw_ips = re.findall(r'\d+\.\d+\.\d+\.\d+', string)

list_count = {}

for i in raw_ips:
	if i not in list_count:
		list_count[i] = 0
	list_count[i] += 1

result = sorted(list_count.items(), key=lambda x:x[1], reverse=True)
for i in range(5):
	print(result[i])