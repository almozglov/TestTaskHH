import re

# Данный код ищет в списке ссылок пять самых часто встречаемых IP адреса

file = open('test2.txt')

# Т.к. python читает файлы посимвольно, данный цикл переносит всё содержимое
# файла в переменную string

string = ''
for i in file:
	string += i

# При помощи регулярных выражений идёт поиск всех строк, соответствующих шаблону
# IP-адреса ((несколько чисел).(несколько чисел).(несколько чисел).(несколько чисел))
raw_ips = re.findall(r'\d+\.\d+\.\d+\.\d+', string)

list_count = {}

# Данный цикл составляет словарь уникальный адресов, и считает, сколько раз они
# появлялись в исходном файле 
for i in raw_ips:
	if i not in list_count:
		list_count[i] = 1
	list_count[i] += 1

#Сортировка словаря по убыванию. 
result = sorted(list_count.items(), key=lambda x:x[1], reverse=True)

for i in range(5):
	print(result[i][0])